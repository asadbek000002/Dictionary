from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, F, Count
from .models import Text, Suffix, News, UsefulLink, Words, Employees, SearchHistory, Regions, Contact, Publications, \
    About, CategoryProject
from .serializers import NewsListSerializer, UsefulLinkSerializer, NewsDetailSerializer, UsefulLinkLatestSerializer, \
    EmployeesListSerializer, RegionStatisticsSerializer, ContactSerializer, PublicationsSerializer, \
    TextDetailSerializer, AboutSerializer, CategoryProjectSerializer, CategoryProjectDetailSerializer
import re


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
            matched_suffix = None

            for suffix in Suffix.objects.all():
                if root.endswith(suffix.suffix):  # Agar so'z qo'shimchani tugatsa
                    # Eng uzun mos keluvchi qo'shimchani tanlash
                    if not matched_suffix or len(suffix.suffix) > len(matched_suffix.suffix):
                        matched_suffix = suffix

            if matched_suffix:
                suffix_objs.append(matched_suffix)  # Qo'shimchani qo'shish
                root = root[:-len(matched_suffix.suffix)]  # Ildizni yangilash (qo'shimchani olib tashlash)
            else:
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
        # Matndagi barcha so'zlarni tartib bilan olish
        word_matches = re.finditer(r'\b\w+\b', text.content)

        for match in word_matches:
            word = match.group()  # So'zning o'zi
            start_idx = match.start()  # So'zning boshlanish indeksi
            end_idx = match.end()  # So'zning tugash indeksi

            if search_type == "token" and word.lower().startswith(prefix.lower()):
                # Token qidiruvi: prefix bilan boshlanadigan so'zlarni tekshirish
                suffix_info = self.get_suffix_info(word)

                matches.append({
                    "word": word,
                    "start_idx": start_idx,
                    "end_idx": end_idx,
                    "root": suffix_info['root'],  # Faqat ildizni qaytarish
                    "suffixes": suffix_info['suffixes'],  # Barcha qo'shimchalarni qaytarish
                })
            elif search_type == "lemma" and word.lower() == prefix.lower():
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
            "source": text.source,
            "content": text.content,
            "matches": matches
        }

    def count_word_occurrences(self, prefix, search_type):
        """
        Barcha matnlar bo'ylab qidiruv so'zining umumiy uchrash sonini aniqlash.
        """
        total_count = 0

        # Text obyektlarining barchasini olish
        texts = Text.objects.all()

        for text in texts:
            word_matches = re.finditer(r'\b\w+\b', text.content)

            for match in word_matches:
                word = match.group()
                if search_type == "token" and word.lower().startswith(prefix.lower()):
                    total_count += 1  # Prefiks bilan mos kelgan so'zni hisoblash
                elif search_type == "lemma" and word.lower() == prefix.lower():
                    total_count += 1  # To'liq mos kelgan so'zni hisoblash

        return total_count

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

        if text_id:
            text = Text.objects.filter(id=text_id).first()
            if text:
                word = text.word
                word_details = self.get_word_details(word)
                result = self.process_text(text, prefix, search_type)
                if result:
                    result = {"word_details": word_details, **result}
                    return Response(result)
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Text topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        word = Words.objects.filter(name__iexact=prefix).first()  # Bitta obyektni oladi
        if not word:
            return Response({"error": "So'z topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        word_details = self.get_word_details(word)
        texts = Text.objects.filter(word=word).order_by('pk')
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

        total_occurrences = self.count_word_occurrences(prefix, search_type)

        return paginator.get_paginated_response({
            "word_details": word_details,
            "text_count": text_count,
            "total_occurrences": total_occurrences,
            "search_results": results
        })

    def get_word_details(self, word):
        if not word:
            return None
        return {
            "name": word.name,
            "grammatical_description": word.grammatical_description,
            "lexical_form": word.lexical_form,
            "comment": word.comment,
        }


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
        latest_useful_link = UsefulLink.objects.all()[:4]
        total_count = UsefulLink.objects.count()
        remaining_count = max(total_count - 4, 0)
        serializer = UsefulLinkLatestSerializer(latest_useful_link, many=True, context={"request": request})
        return Response({
            "count": remaining_count,
            "latest_useful_links": serializer.data
        })


# Employees

class EmployeesListAPIView(ListAPIView):
    queryset = Employees.objects.all().order_by(
        F('order').asc(nulls_last=True))  # So'nggi qo'shilganlar yuqorida bo'ladi
    serializer_class = EmployeesListSerializer
    pagination_class = Pagination


# Top Search

class TopSearchHistoryView(APIView):
    def get(self, request):
        # Eng ko'p qidirilgan 10 ta so'zni olish
        top_search_histories = SearchHistory.objects.filter(word__isnull=False).exclude(word=None).order_by('-count')[
                               :5]

        results = []

        # Har bir so'zga tegishli bitta textni olish
        for search_history in top_search_histories:
            word = search_history.word  # So'z
            if word:
                text = Text.objects.filter(word=word).first()
                results.append({
                    'text_id': text.id if text else None,
                    'word': word.name,
                    'count': search_history.count,
                    'text': text.content[:150] if text else None,
                })
            else:
                results.append({
                    'word': None,
                    'count': search_history.count,
                    'text': None,
                })

        return Response({'top_search_histories': results})


def save_search_history(prefix):
    try:
        # So'zni topish
        word = Words.objects.filter(name=prefix.lower()).first()

        if word:
            search_history, created = SearchHistory.objects.get_or_create(word=word)
        else:
            search_history, created = SearchHistory.objects.get_or_create(missing_word=prefix)

        if created:
            search_history.count = 1
        else:
            search_history.count = F('count') + 1

        search_history.save()
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")


class TopSearchDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            news = Text.objects.get(id=pk)
            serializer = TextDetailSerializer(news, context={"request": request})
            return Response(serializer.data)
        except Text.DoesNotExist:
            return Response({"error": "text topilmadi."}, status=status.HTTP_404_NOT_FOUND)


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


# About
class LatestAboutAPIView(RetrieveAPIView):
    serializer_class = AboutSerializer

    def get_object(self):
        return About.objects.all().order_by('-id').first()


# About Project
class CategoryListAPIView(ListAPIView):
    queryset = CategoryProject.objects.all()
    serializer_class = CategoryProjectSerializer


class CategoryDetailAPIView(RetrieveAPIView):
    queryset = CategoryProject.objects.all()
    serializer_class = CategoryProjectDetailSerializer
