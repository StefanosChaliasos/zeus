"""
A collection of helper model mixins to decouple election/poll state identifiers
"""

import datetime

from collections import defaultdict
from functools import wraps

FEATURES_REGISTRY = defaultdict(dict)
LOCAL_MIXES_COUNT = 1


def feature(ns, *features):

    if not ns in FEATURES_REGISTRY:
        FEATURES_REGISTRY[ns] = {}

    def wrapper(func):
        _features = features
        if len(features) == 0:
            _features = [func.__name__.replace(
                '_feature_', '').replace('_feature', '')]
        for feature in _features:
            if not feature in FEATURES_REGISTRY[ns]:
                FEATURES_REGISTRY[ns][feature] = []
            FEATURES_REGISTRY[ns][feature].append(func)

        @wraps(func)
        def inner(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        return inner
    return wrapper


class FeaturesMixin(object):

    def __getattr__(self, name, *args, **kwargs):
        if name.startswith('feature_'):
            feature = name.replace('feature_', '')
            return self.check_feature(feature)
        return super(FeaturesMixin, self).__getattribute__(name, *args,
                                                           **kwargs)

    def check_feature(self, feature):
        if feature in FEATURES_REGISTRY[self.features_ns]:
            feature_checks = FEATURES_REGISTRY[self.features_ns][feature]
            return all([f(self) for f in feature_checks])
        raise Exception("Invalid feature key (%s)" % feature)

    def check_features(self, *features):
        return all([self.check_feature(f) for f in features])

    def check_features_verbose(self, *features):
        return [(f, self.check_feature(f)) for f in features]

    def list_features(self):
        return FEATURES_REGISTRY.get(self.features_ns).keys()


def election_feature(*args):
    return feature('election', *args)


def poll_feature(*args):
    return feature('poll', *args)


class ElectionFeatures(FeaturesMixin):

    features_ns = 'election'

    def __getattr__(self, name, *args, **kwargs):
        if name.startswith('polls_feature_'):
            feature = name.replace('polls_feature_', '')
            return self.polls_feature(feature)
        if name.startswith('any_poll_feature_'):
            feature = name.replace('any_poll_feature_', '')
            return any(self.polls_feature_iter(feature))
        return FeaturesMixin.__getattr__(self, name, *args, **kwargs)

    def polls_feature(self, *args, **kwargs):
        results = [bool(poll.check_features(*args))
                   for poll in self.polls.all()]
        nr_polls = len(results)
        return nr_polls > 0 and sum(results) == nr_polls

    def polls_feature_iter(self, *args, **kwargs):
        result = True
        for poll in self.polls.all():
            yield poll.check_features(*args)

    @election_feature()
    def _feature_can_upload_remote_mix(self):
        return self.feature_can_close_remote_mixing

    @election_feature()
    def _feature_can_close_remote_mixing(self):
      return self.mix_key and \
        self.polls_feature_mix_finished and \
        not self.feature_remote_mixing_finished

    @election_feature()
    def _feature_voting_started(self):
      return  self.feature_frozen and \
              self.voting_starts_at <= datetime.datetime.now()

    @election_feature()
    def _feature_canceled(self):
        return self.canceled_at

    @election_feature()
    def _feature_can_edit(self):
        return not self.feature_completed

    @election_feature()
    def _feature_editing(self):
        return self.feature_can_edit

    @election_feature()
    def _feature_completed(self):
        return self.feature_canceled or self.completed_at

    @election_feature('edit_voting_extended_until', 'edit_remote_mixes')
    def _feature_edit_fields3(self):
        return not self.feature_closed

    @election_feature('edit_trustees', 'edit_name', 'edit_description',
                      'edit_type', 'edit_voting_starts_at',
                      'edit_voting_ends_at', 'remote_mixes',
                      'edit_trial', 'edit_departments')
    def _feature_editing_fields(self):
        return not self.feature_frozen

    @election_feature('edit_cast_consent_text')
    def _feature_editing_cast_consent_text(self):
        return not self.feature_voting_started

    @election_feature('edit_help_email', 'edit_help_phone')
    def _feature_editing_fields2(self):
        return not self.feature_frozen

    @election_feature()
    def _feature_pending_polls_issues(self):
        return self.polls_feature('pending_issues')

    @election_feature()
    def _feature_delete_trustee(self):
        return not self.feature_frozen

    @election_feature()
    def _feature_delete_trustee(self):
        return not self.feature_frozen

    @election_feature()
    def _feature_pending_issues(self):
        pending = len(self.election_issues_before_freeze) > 0
        return pending or self.feature_pending_polls_issues

    @election_feature()
    def _feature_can_add_poll(self):
        return (not self.feature_frozen) and self.get_module().can_edit_polls()

    @election_feature()
    def _feature_can_rename_poll(self):
        return not self.feature_voting_started

    @election_feature()
    def _feature_can_send_trustee_email(self):
        # TODO: Fine grain status check
        return not self.feature_completed

    @election_feature('can_send_trustee_email', 'trustee_can_login',
                      'trustee_can_access_election')
    def _feature_trustee_can_login(self):
        return not self.feature_completed

    @election_feature('trustee_can_generate_key', 'trustee_can_upload_pk')
    def _feature_trustee_checks(self):
        return not self.feature_completed and not self.feature_frozen

    @election_feature()
    def _feature_trustee_can_check_sk(self):
        return True

    @election_feature('trustee_can_generate_key', 'trustee_can_upload_pk')
    def _feature_trustee_checks(self):
        return not self.feature_completed and not self.feature_frozen

    @election_feature('trustee_can_check_sk')
    def _feature_trustee_can_(self):
        return not self.feature_completed

    @election_feature()
    def _feature_can_cancel(self):
        return not self.feature_completed

    @election_feature()
    def _feature_can_freeze(self):
        return not self.feature_frozen and not \
               self.feature_pending_issues and not self.feature_completed

    @election_feature()
    def _feature_frozen(self):
        return self.frozen_at

    @election_feature()
    def _feature_voting_date_passed(self):
        return datetime.datetime.now() >= self.voting_end_date

    @election_feature()
    def _feature_within_voting_date(self):
        return datetime.datetime.now() > self.voting_starts_at and \
               datetime.datetime.now() < self.voting_end_date

    @election_feature()
    def _feature_voting(self):
        return self.feature_frozen and self.feature_within_voting_date \
                and not self.feature_completed and not self.feature_closed

    @election_feature()
    def _feature_voting_finished(self):
      return self.feature_frozen and not self.feature_voting

    @election_feature()
    def _feature_can_close(self):
        if self.feature_completed:
            return False

        date_passed_check = self.feature_voting_date_passed
        if self.trial:
            date_passed_check = True

        return self.feature_frozen and date_passed_check and \
               not self.voting_ended_at

    @election_feature()
    def _feature_can_mix(self):
        return self.feature_closed and any(self.polls_feature_iter('can_mix'))

    @election_feature()
    def _feature_mixing(self):
        return any(self.polls_feature_iter('mixing'))

    @election_feature()
    def _feature_mixing_finished(self):
        return self.polls_feature('mixing_finished')

    @election_feature()
    def _feature_remote_mixing_finished(self):
        if not self.mix_key:
            return True
        return self.remote_mixing_finished_at

    @election_feature()
    def _feature_closed(self):
        return self.voting_ended_at

    @election_feature()
    def _feature_polls_results_computed(self):
        return self.polls_feature_compute_results_finished


class PollFeatures(FeaturesMixin):

    features_ns = 'poll'

    # Forum related features
    @poll_feature()
    def _feature_can_register_for_forum_updates(self):
        return self.feature_forum_open

    @poll_feature()
    def _feature_edit_forum(self):
        return not self.feature_frozen and not self.linked_ref

    @poll_feature()
    def _feature_edit_name(self):
        return not self.feature_frozen

    @poll_feature()
    def _feature_edit_forum_extension(self):
        return self.feature_frozen and not self.election.feature_closed

    @poll_feature()
    def _feature_can_sync_voters(self):
        return self.election.feature_can_add_poll

    @poll_feature()
    def _feature_edit_taxisnet(self):
        return not self.feature_frozen

    @poll_feature()
    def _feature_edit_linked_ref(self):
        existing = self.pk
        has_voters = existing
        if existing:
            has_voters = self.voters.count() > 0
        return not self.election.feature_closed and not has_voters

    @poll_feature()
    def _feature_forum_closed(self):
        return self.election.feature_closed

    @poll_feature()
    def _feature_forum_visible(self):
        return self.forum_enabled

    @poll_feature()
    def _feature_forum_started(self):
        return self.feature_forum_visible \
            and self.forum_starts_at <= datetime.datetime.now() \
            and self.feature_frozen

    @poll_feature()
    def _feature_forum_posts_visible(self):
        return self.feature_forum_started

    @poll_feature()
    def _feature_forum_ended(self):
        return (self.forum_end_date < datetime.datetime.now()) or self.election.feature_closed

    @poll_feature()
    def _feature_forum_can_post(self):
        return self.feature_forum_open

    @poll_feature()
    def _feature_forum_open(self):
        return self.feature_forum_visible and \
            self.feature_frozen and \
            self.feature_forum_started and \
            not self.feature_forum_ended

    # END forum related features

    @poll_feature()
    def _feature_can_edit(self):
        return (not self.election.feature_closed) and self.get_module().can_edit_polls()

    @poll_feature()
    def _feature_can_manage_questions(self):
        return not self.feature_voting_started

    @poll_feature()
    def _feature_can_preview_booth(self):
        return not self.feature_validate_voting_finished

    @poll_feature()
    def _feature_can_remove(self):
        return (not self.feature_frozen) and self.get_module().can_edit_polls()

    @poll_feature()
    def _feature_can_add_voter(self):
        return not self.election.feature_closed and not self.is_linked_leaf

    @poll_feature()
    def _feature_can_clear_voters(self):
        return not self.election.feature_frozen and not \
               self.election.feature_completed and not self.is_linked_leaf

    @poll_feature()
    def _feature_voters_set(self):
        return self.voters.count() > 0

    @poll_feature()
    def _feature_voters_imported(self):
        return self.voters.count() > 0

    @poll_feature()
    def _feature_questions_added(self):
        return len(self.questions_data) > 0

    @poll_feature()
    def _feature_can_delete(self):
        return self.voters.count() == 0

    @poll_feature()
    def _feature_public_results(self):
        return False

    @poll_feature()
    def _feature_voting_started(self):
      return bool(self.election.frozen_at) and \
              self.election.voting_starts_at <= datetime.datetime.now()

    @poll_feature()
    def _feature_votes_cast(self):
        return self.cast_votes.count() > 0

    @poll_feature()
    def _feature_can_send_voter_mail(self):
        return not self.is_linked_leaf and not self.election.canceled_at and self.voters.count() > 0

    @poll_feature()
    def _feature_can_send_voter_booth_invitation(self):
        return self.election.feature_frozen and not \
               self.election.feature_closed

    @poll_feature()
    def _feature_can_cast_vote(self):
        return self.election.feature_voting

    @poll_feature()
    def _feature_pending_issues(self):
        return len(self.issues_before_freeze) > 0

    @poll_feature()
    def _feature_can_freeze(self):
        return not self.frozen_at

    @poll_feature()
    def _feature_frozen(self):
        return self.frozen_at

    @poll_feature()
    def _feature_can_exclude_voter(self):
        if self.is_linked_leaf:
            return False
        return not self.election.feature_closed

    @poll_feature()
    def _feature_can_delete_voter(self):
        if self.is_linked_leaf:
            return False
        if self.election.feature_closed:
            return False
        return self.get_module().can_delete_poll_voters()

    @poll_feature()
    def _feature_can_mix(self):
        closed = self.election.feature_closed
        mixing = self.feature_mix_running
        finished = self.feature_mix_finished
        return closed and not mixing and not finished

    @poll_feature()
    def _feature_remote_mixes_finished(self):
        if not self.election.mix_key:
            return True
        else:
            return bool(self.election.remote_mixing_finished_at)

    @poll_feature()
    def _feature_mixing_finished(self):
        remote_finished = self.feature_remote_mixes_finished
        return remote_finished and self.feature_mix_finished

    @poll_feature()
    def _feature_closed(self):
        return self.election.feature_closed

    @poll_feature()
    def _feature_partial_decryptions_finished(self):
        return self.feature_partial_decrypt_finished and \
               self.feature_zeus_partial_decrypt_finished


class VoterFeatures(FeaturesMixin):
    pass


class TrusteeFeatures(FeaturesMixin):
    pass
