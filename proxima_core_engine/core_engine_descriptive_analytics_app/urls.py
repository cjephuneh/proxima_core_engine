from django.urls import include, path, re_path

from core_engine_descriptive_analytics_app.views import (
    CommunicationChannels, EngagementFrequency, LeastEngagedTopics, HourlyAverageResponseTime, AverageResponseTime, ClientSatisfaction,
    ClientHourlyClientSatisfaction, MostPopularTopics, ClientsAverageAge, CityDistribution, CountryDistribution,
    GenderDistribution, StateDistribution, AverageCommentsPerThread, CommunityGrowthRate, CommunityMembers,
    CommunityRating, CumulativeComments, CountEscalatedIssues, CountHourlyEscalatedIssues, CumulativeIssues,
    UniqueComments, CountAllChats, CumulativeCountAllHourlyChats, CountAllHourlyChats, CumulativeVoiceMessages,
    AverageVoiceMessagePerchat, IssueUserRelation, CommentsUserRelation, SurveyRatings, SurveyResponseRate, AverageSurveyRunPeriod,
    TotalSurveys
)

app_name="core_engine_descriptive_analytics_app"


urlpatterns = [
    re_path(r'^api/analytics/', include([
        # Signin
        re_path(r'^countchats/$', CountAllChats.as_view(), name='core_analytics_countchats'),
        re_path(r'^cumulativehourlychats/$', CumulativeCountAllHourlyChats.as_view(), name='core_analytics_cumulativehourlychats'),
        re_path(r'^counthourlychats/$', CountAllHourlyChats.as_view(), name='core_analytics_counthourlychats'),
        re_path(r'^countescalatedissues/$', CountEscalatedIssues.as_view(), name='core_analytics_countescalatedissues'),
        re_path(r'^hourlycountescalatedissues/$', CountHourlyEscalatedIssues.as_view(), name='core_analytics_hourlycountescalatedissues'),
        re_path(r'^communicationchannels/$', CommunicationChannels.as_view(), name='core_analytics_communicationchannels'),
        re_path(r'^engagementfrequency/$', EngagementFrequency.as_view(), name='core_analytics_engagementfrequency'),
        re_path(r'^hourlyaverageresponsetime/$', HourlyAverageResponseTime.as_view(), name='core_analytics_hourlyaverageresponsetime'),
        re_path(r'^averageresponsetime/$', AverageResponseTime.as_view(), name='core_analytics_averageresponsetime'),
        re_path(r'^hourlyclientsatisfaction/$', ClientHourlyClientSatisfaction.as_view(), name='core_analytics_hourly_clientsatisfaction'),
        re_path(r'^leasttopics/$', LeastEngagedTopics.as_view(), name='core_analytics_leasttopics'),
        re_path(r'^clientsatisfaction/$', ClientSatisfaction.as_view(), name='core_analytics_clientsatisfaction'),
        re_path(r'^populartopics/$', MostPopularTopics.as_view(), name='core_analytics_populartopics'),
        re_path(r'^clientsaverageage/$', ClientsAverageAge.as_view(), name='core_analytics_clientsaverageage'),
        re_path(r'^clientcitydistribution/$', CityDistribution.as_view(), name='core_analytics_clientcitydistribution'),
        re_path(r'^countrydistribution/$', CountryDistribution.as_view(), name='core_analytics_countrydistribution'),
        re_path(r'^genderdistribution/$', GenderDistribution.as_view(), name='core_analytics_genderdistribution'),
        re_path(r'^statedistribution/$', StateDistribution.as_view(), name='core_analytics_statedistribution'),
        re_path(r'^averagecomments/$', AverageCommentsPerThread.as_view(), name='core_analytics_averagecomments'),
        re_path(r'^communitygrowthrate/$', CommunityGrowthRate.as_view(), name='core_analytics_communitygrowthrate'),
        re_path(r'^communitymembers/$', CommunityMembers.as_view(), name='core_analytics_communitymembers'),
        re_path(r'^communityrating/$', CommunityRating.as_view(), name='core_analytics_communityrating'),
        re_path(r'^cumulativecomments/$', CumulativeComments.as_view(), name='core_analytics_cumulativecomments'),
        re_path(r'^cumulativeissues/$', CumulativeIssues.as_view(), name='core_analytics_cumulativeissues'),
        re_path(r'^uniquecomments/$', UniqueComments.as_view(), name='core_analytics_uniquecomments'),
        re_path(r'^cumulativevoicemessage/$', CumulativeVoiceMessages.as_view(), name='core_analytics_cumulativevoicemessage'),
        re_path(r'^averagevoicemessageperchat/$', AverageVoiceMessagePerchat.as_view(), name='core_analytics_averagevoicemessageperchat'),
        re_path(r'^issueuserrelation/$', IssueUserRelation.as_view(), name='core_analytics_issueuserrelation'),
        re_path(r'^commentsuserrelation/$', CommentsUserRelation.as_view(), name='core_analytics_commentsuserrelation'),
        re_path(r'^surveyratings/$', SurveyRatings.as_view(), name='core_analytics_surveyratings'),
        re_path(r'^surveyresponserate/$', SurveyResponseRate.as_view(), name='core_analytics_surveyresponserate'),
        re_path(r'^averagesurveyrunperiod/$', AverageSurveyRunPeriod.as_view(), name='core_analytics_averagesurveyrunperiod'),
        re_path(r'^totalsurveys/$', TotalSurveys.as_view(), name='core_analytics_totalsurveys'),

    ]))
]