from django.conf.urls import url

from MATOM import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.HomePageView.as_view(),
        name='index'),
    url(
        regex=r'documentation/$',
        view=views.DocumentationView.as_view(),
        name='documentation'
    ),
    url(
        regex=r'downloads/$',
        view=views.DownloadsView.as_view(),
        name='downloads'
    ),

    url(
        regex=r'about/$',
        view=views.AboutView.as_view(),
        name='about'
    ),

    url(
        regex=r'comparison/$',
        view=views.AssessByComparisonView.as_view(),
        name='comparison'),

    url(
        regex=r'comparison/job(\d+)$',
        view=views.GetResultsCompare.as_view(),
        name="compare-results"),

    url(
        regex=r'^score/$',
        view=views.AssessByScoreView.as_view(),
        name="score"),

    url(
        regex=r'score/job(\d+)$',
        view=views.GetResultsScore.as_view(),
        name="score-results"),

    url(
        regex=r'enrichment/$',
        view=views.AssessByEnrichmentView.as_view(),
        name="enrichment"),

    url(
        regex=r'enrichment/job(\d+)$',
        view=views.GetResultsEnrich.as_view(),
        name="enrichment-results"),

    # url(
    #     regex=r'search/$',
    #     view=search_views.SearchView.as_view(),
    #     name='search'),

    url(
        regex=r'search/$',
        view=views.SearchView.as_view(),
        name='search'
    ),

    url(
        regex=r'search/select/$',
        view=views.SearchResultsView.as_view(),
        name='search-select'
    )

]
