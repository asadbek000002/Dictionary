from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Text, Suffix, News, UsefulLink
from .serializers import TextSerializer, SuffixSerializer, NewsListSerializer, UsefulLinkSerializer


class SearchPagination(PageNumberPagination):
    page_size = 8  # Har sahifada nechta natija bo'lishi kerak
    page_size_query_param = 'page_size'
    max_page_size = 100


class NewsPagination(PageNumberPagination):
    page_size = 10  # Har bir sahifada 10 ta yangilik
    page_size_query_param = 'page_size'
    max_page_size = 100


class SearchAndSuffixAPIView(APIView):
    pagination_class = SearchPagination

    def get_suffix_info(self, word):
        """
        So'zning ildizini va barcha qo'shimchalarini aniqlash.
        """
        suffix_objs = []  # Topilgan barcha qo'shimchalar
        root = word  # So'zning boshlang'ich holati
        while root:  # So'zni oxirigacha tekshirish
            matched = False
            for suffix in Suffix.objects.all():
                if root.endswith(suffix.suffix):  # Agar so'z qo'shimchani tugatsa
                    suffix_objs.append(suffix)  # Qo'shimchani qo'shish
                    root = root[:-len(suffix.suffix)]  # Ildizni yangilash (qo'shimchani olib tashlash)
                    matched = True
                    break  # Birinchi mos qo'shimchani topgandan so'ng davom etish

            if not matched:
                break  # Qo'shimcha topilmasa, davom etishni to'xtatish

        # Agar hech qanday qo'shimcha topilmasa, to'liq so'zni ildiz sifatida qaytaramiz
        return {
            "root": root,  # So'zning ildizi
            "suffixes": [{"suffix": suffix.suffix, "suffix_description": suffix.description} for suffix in suffix_objs]
        }

    def process_text(self, text, prefix, search_type):
        """
        Matnni tahlil qilish va so'zlarni ajratish, har bir so'zga qo'shimchalarni aniqlash.
        """
        matches = []
        words = text.content.split()
        for word in words:
            start_idx = text.content.lower().find(word.lower())
            end_idx = start_idx + len(word)

            if search_type == "token" and word.lower().startswith(prefix):
                # Token qidiruvi: prefix bilan boshlanadigan so'zlarni tekshirish
                suffix_info = self.get_suffix_info(word)

                matches.append({
                    "word": word,
                    "start_idx": start_idx,
                    "end_idx": end_idx,
                    "root": suffix_info['root'],  # Faqat ildizni qaytarish
                    "suffixes": suffix_info['suffixes'],  # Barcha qo'shimchalarni qaytarish
                })
            elif search_type == "lemma" and word.lower() == prefix:
                matches.append({
                    "word": word,
                    "start_idx": start_idx,
                    "end_idx": end_idx,
                })

        # Agar mosliklar bo'lmasa, hech qanday natija qaytarmaymiz
        if not matches:
            return None  # Natija bo'lmasa, `None` qaytarish

        return {
            "id": text.id,
            "content": text.content,
            "matches": matches,
        }

    def get(self, request):
        """
        GET so'rovi orqali qidiruv va qo'shimcha ma'lumotlarni qaytarish.
        """
        prefix = request.GET.get('prefix', '').lower()  # Qidiruv so'zi
        search_type = request.GET.get('search_type', '').lower()  # Qidiruv turi

        # Agar qidiruv so'zi bo'lmasa, hech qanday xato qaytarmasdan bo'sh natija
        if not prefix or not search_type:
            return Response(status=status.HTTP_204_NO_CONTENT)  # Hech qanday natija bo'lmasa, bo'sh javob qaytaramiz

        if search_type not in ["token", "lemma"]:
            return Response({"error": "search_type faqat 'token' yoki 'lemma' bo'lishi mumkin."},
                            status=status.HTTP_400_BAD_REQUEST)

        texts = Text.objects.filter(content__icontains=prefix)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(texts, request)

        # Matnlarni qayta ishlash
        results = [self.process_text(text, prefix, search_type) for text in result_page]

        # Hech qanday moslik bo'lmasa, bo'sh javob qaytarish
        results = [result for result in results if result is not None]

        # Agar hech qanday natija bo'lmasa, 204 No Content qaytarish
        if not results:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return paginator.get_paginated_response({"search_results": results})


class SuffixInfoAPIView(APIView):
    """
    Qo'shimcha haqida ma'lumot olish.
    """

    def get(self, request):
        suffix = request.GET.get('suffix', '').lower()
        if not suffix:
            return Response({"error": "Qo'shimcha kiritilishi kerak."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            suffix_obj = Suffix.objects.get(suffix=suffix)
            serializer = SuffixSerializer(suffix_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Suffix.DoesNotExist:
            return Response({"error": "Qo'shimcha topilmadi."}, status=status.HTTP_404_NOT_FOUND)


# News

class NewsListAPIView(ListAPIView):
    queryset = News.objects.all().order_by('-created_at')  # So'nggi qo'shilganlar yuqorida bo'ladi
    serializer_class = NewsListSerializer
    pagination_class = NewsPagination


class LatestNewsAPIView(APIView):
    def get(self, request):
        latest_news = News.objects.all().order_by('-created_at')[:6]
        serializer = NewsListSerializer(latest_news, many=True)
        return Response(serializer.data)


# Havola


class UsefulLinkListAPIView(ListAPIView):
    queryset = UsefulLink.objects.all()  # So'nggi qo'shilganlar yuqorida bo'ladi
    serializer_class = UsefulLinkSerializer
    pagination_class = NewsPagination


class LatestUsefulLinkAPIView(APIView):
    def get(self, request):
        latest_useful_link = UsefulLink.objects.all()[:6]
        serializer = UsefulLinkSerializer(latest_useful_link, many=True)
        return Response(serializer.data)
