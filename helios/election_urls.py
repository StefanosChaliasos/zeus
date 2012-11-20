"""
Helios URLs for Election related stuff

Ben Adida (ben@adida.net)
"""

from django.conf.urls.defaults import *

from helios.views import *

urlpatterns = patterns('',
    (r'^$', one_election),

    # edit election params
    (r'^/edit$', one_election_edit),
    (r'^/schedule$', one_election_schedule),
    (r'^/archive$', one_election_archive),

    (r'^/stats$', one_election_public_stats),

    # badge
    (r'^/badge$', election_badge),

    # adding trustees
    (r'^/trustees/$', list_trustees),
    (r'^/trustees/view$', list_trustees_view),
    (r'^/trustees/new$', new_trustee),
    (r'^/trustees/add-helios$', new_trustee_helios),
    (r'^/trustees/delete$', delete_trustee),

    # trustee pages
    (r'^/trustees/(?P<trustee_uuid>[^/]+)/home$', trustee_home),
    (r'^/trustees/(?P<trustee_uuid>[^/]+)/sendurl$', trustee_send_url),
    (r'^/trustees/(?P<trustee_uuid>[^/]+)/keygenerator$', trustee_keygenerator),
    (r'^/trustees/(?P<trustee_uuid>[^/]+)/check-sk$', trustee_check_sk),
    (r'^/trustees/(?P<trustee_uuid>[^/]+)/upload-pk$', trustee_upload_pk),
    (r'^/trustees/(?P<trustee_uuid>[^/]+)/decrypt-and-prove$', trustee_decrypt_and_prove),
    (r'^/trustees/(?P<trustee_uuid>[^/]+)/download-ciphers$', trustee_download_ciphers),
    (r'^/trustees/(?P<trustee_uuid>[^/]+)/upload-decryption$', trustee_upload_decryption),
    (r'^/trustees/(?P<trustee_uuid>[^/]+)/verify-key$', trustee_verify_key),

    # election voting-process actions
    (r'^/view$', one_election_view),
    (r'^/post-ecounting$', election_post_ecounting),
    (r'^/result$', one_election_result),
    (r'^/result_proof$', one_election_result_proof),
    (r'^/zeus-proofs.zip$', election_zeus_proofs),
    # (r'^/bboard$', one_election_bboard),
    (r'^/audited-ballots/$', one_election_audited_ballots),

    # get randomness
    (r'^/get-randomness$', get_randomness),

    # server-side encryption
    (r'^/encrypt-ballot$', encrypt_ballot),

    # construct election
    (r'^/questions$', one_election_questions),
    (r'^/set_reg$', one_election_set_reg),
    (r'^/set_featured$', one_election_set_featured),
    (r'^/save_questions$', one_election_save_questions),
    (r'^/register$', one_election_register),
    (r'^/freeze$', one_election_freeze), # includes freeze_2 as POST target

    # computing tally
    (r'^/compute_tally$', one_election_compute_tally),
    (r'^/cancel$', one_election_cancel),
    (r'^/set-completed', one_election_set_completed),
    (r'^/report\.(?P<format>[a-z]+)$', election_report),
    (r'^/mix/(?P<mix_key>.*)$', election_remote_mix),
    (r'^/remove_last_mix$', election_remove_last_mix),
    (r'^/stop-mixing$', election_stop_mixing),
    (r'^/combine_decryptions$', combine_decryptions),

    # casting a ballot before we know who the voter is
    (r'^/cast$', one_election_cast),
    (r'^/cast_confirm$', one_election_cast_confirm),
    (r'^/password_voter_login$', password_voter_login),
    (r'^/l/(?P<voter_uuid>.*)/(?P<voter_secret>.*)$', voter_quick_login),
    (r'^/cast_done$', one_election_cast_done),
    (r'^/s/(?P<fingerprint>.*)$', one_election_download_signature),

    # post audited ballot
    (r'^/post-audited-ballot', post_audited_ballot),

    # managing voters
    (r'^/voters/$', voter_list),
    (r'^/voters/csv$', voters_csv),
    (r'^/voters/clear$', voters_clear),
    (r'^/voters/upload$', voters_upload),
    (r'^/voters/upload-cancel$', voters_upload_cancel),
    (r'^/voters/list$', voters_list_pretty),
    (r'^/voters/eligibility$', voters_eligibility),
    (r'^/voters/email$', voters_email),
    (r'^/voters/(?P<voter_uuid>[^/]+)$', one_voter),
    (r'^/voters/(?P<voter_uuid>[^/]+)/delete$', voter_delete),
    (r'^/voters/(?P<voter_uuid>[^/]+)/exclude$', voter_exclude),

    # ballots
    (r'^/ballots/$', ballot_list),
    (r'^/ballots/(?P<voter_uuid>[^/]+)/all$', voter_votes),
    (r'^/ballots/(?P<voter_uuid>[^/]+)/last$', voter_last_vote),

)
