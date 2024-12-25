from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, F, Count
from .models import Text, Suffix, News, UsefulLink, Words, Employees, SearchHistory, Regions, Contact, Publications
from .serializers import NewsListSerializer, UsefulLinkSerializer, NewsDetailSerializer, UsefulLinkDetailSerializer, \
    EmployeesListSerializer, RegionStatisticsSerializer, ContactSerializer, PublicationsSerializer, EmployeesDetailSerializer


class Pagination(PageNumberPagination):
    page_size = 10  # Har sahifada nechta natija bo'lishi kerak
    page_size_query_param = 'page_size'
    max_page_size = 100


class SearchAndSuffixAPIView(APIView):
    pagination_class = Pagination

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
            # word_count += 1

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
                    # "start_idx": start_idx,
                    # "end_idx": end_idx,
                })

        # Agar mosliklar bo'lmasa, hech qanday natija qaytarmaymiz
        if not matches:
            return None  # Natija bo'lmasa, `None` qaytarish

        return {
            "id": text.id,
            "source": text.source,
            "content": text.content,
            "matches": matches
        }

    def get(self, request):
        """
        GET so'rovi orqali qidiruv va qo'shimcha ma'lumotlarni qaytarish.
        """
        prefix = request.GET.get('prefix', '').lower()  # Qidiruv so'zi
        search_type = request.GET.get('search_type', '').lower()  # Qidiruv turi
        text_id = request.GET.get('text_id', None)

        # Agar qidiruv so'zi bo'lmasa, hech qanday xato qaytarmasdan bo'sh natija
        if not prefix or not search_type:
            return Response(status=status.HTTP_204_NO_CONTENT)  # Hech qanday natija bo'lmasa, bo'sh javob qaytaramiz

        if search_type not in ["token", "lemma"]:
            return Response({"error": "search_type faqat 'token' yoki 'lemma' bo'lishi mumkin."},
                            status=status.HTTP_400_BAD_REQUEST)

        if prefix:
            save_search_history(prefix)  # Qidiruv so'zini saqlash

        # Agar bitta textni olishni xohlasangiz
        if text_id:
            text = Text.objects.filter(id=text_id).first()
            if text:
                result = self.process_text(text, prefix, search_type)
                return Response(result) if result else Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Text topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        word = Words.objects.filter(name__iexact=prefix)
        texts = Text.objects.filter(word__in=word).order_by('pk')
        text_count = texts.count()

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(texts, request)

        # Matnlarni qayta ishlash
        results = [self.process_text(text, prefix, search_type) for text in result_page]

        # Hech qanday moslik bo'lmasa, bo'sh javob qaytarish
        results = [result for result in results if result is not None]

        # Agar hech qanday natija bo'lmasa, 204 No Content qaytarish
        if not results:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return paginator.get_paginated_response({'text_count': text_count, "search_results": results})


# News

class NewsListAPIView(ListAPIView):
    queryset = News.objects.all().order_by('-created_at')  # So'nggi qo'shilganlar yuqorida bo'ladi
    serializer_class = NewsListSerializer
    pagination_class = Pagination


class LatestNewsAPIView(APIView):
    def get(self, request):
        latest_news = News.objects.all().order_by('-created_at')[:6]
        serializer = NewsListSerializer(latest_news, many=True, context={"request": request})
        return Response(serializer.data)


class NewsDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            news = News.objects.get(id=pk)
            serializer = NewsDetailSerializer(news, context={"request": request})
            return Response(serializer.data)
        except News.DoesNotExist:
            return Response({"error": "Yangilik topilmadi."}, status=status.HTTP_404_NOT_FOUND)


# Link


class UsefulLinkListAPIView(ListAPIView):
    queryset = UsefulLink.objects.all()  # So'nggi qo'shilganlar yuqorida bo'ladi
    serializer_class = UsefulLinkSerializer
    pagination_class = Pagination


class LatestUsefulLinkAPIView(APIView):
    def get(self, request):
        latest_useful_link = UsefulLink.objects.all()[:6]
        serializer = UsefulLinkSerializer(latest_useful_link, many=True, context={"request": request})
        return Response(serializer.data)


class UsefulLinkDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            useful_link = UsefulLink.objects.get(id=pk)
            serializer = UsefulLinkDetailSerializer(useful_link, context={"request": request})
            return Response(serializer.data)
        except UsefulLink.DoesNotExist:
            return Response({"error": "Useful Link topilmadi."}, status=status.HTTP_404_NOT_FOUND)


# Employees

class EmployeesListAPIView(ListAPIView):
    queryset = Employees.objects.all().order_by(
        F('order').asc(nulls_last=True))  # So'nggi qo'shilganlar yuqorida bo'ladi
    serializer_class = EmployeesListSerializer
    pagination_class = Pagination


class EmployeesDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            employees = Employees.objects.get(id=pk)
            serializer = EmployeesDetailSerializer(employees, context={"request": request})
            return Response(serializer.data)
        except Employees.DoesNotExist:
            return Response({"error": "employees topilmadi."}, status=status.HTTP_404_NOT_FOUND)


# Top Search

class TopSearchHistoryView(APIView):
    def get(self, request):
        # Eng ko'p qidirilgan 10 ta so'zni olish
        top_search_histories = SearchHistory.objects.filter(word__isnull=False).order_by('-count')[:10]
        print('salom', top_search_histories)

        results = []

        # Har bir so'zga tegishli bitta textni olish
        for search_history in top_search_histories:
            word = search_history.word  # So'z
            # `Text` modelidan `word`ga bog'liq bo'lgan bitta textni olish
            text = Text.objects.filter(word=word).first()

            if text:
                # So'z va tegishli textni natijaga qo'shish
                results.append({
                    'word': word.name,
                    'count': search_history.count,
                    'text': text.content[:150],  # Yoki textda qanday ma'lumot kerakligini chiqarish
                })
            else:
                # Agar `Text` topilmasa, faqat so'zni chiqarish
                results.append({
                    'word': word.name,
                    'count': search_history.count,
                    'text': None,
                })

        return Response({'top_search_histories': results})


def save_search_history(prefix):
    try:
        # So'zni topish
        word = Words.objects.get(name=prefix.lower())
        search_history, created = SearchHistory.objects.get_or_create(word=word)
    except Words.DoesNotExist:
        # So'z mavjud bo'lmasa, missing_word bilan saqlash
        search_history, created = SearchHistory.objects.get_or_create(missing_word=prefix)

    if created:
        search_history.count = 1  # Yangi tarix yaratganda, count 1
    else:
        # Agar so'z allaqon mavjud bo'lsa, count qiymatini oshiramiz
        search_history.count = F('count') + 1

    search_history.save()


# Region Statistic

class RegionStatisticsAPIView(ListAPIView):
    serializer_class = RegionStatisticsSerializer

    def get_queryset(self):
        return Regions.objects.annotate(word_count=Count('words'))


# Contact

class ContactCreateView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


# Publications

class PublicationsAPIView(APIView):
    def get(self, request):
        latest_useful_link = Publications.objects.all()
        serializer = PublicationsSerializer(latest_useful_link, many=True, context={"request": request})
        return Response(serializer.data)
