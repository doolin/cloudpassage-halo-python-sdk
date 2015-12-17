import cloudpassage.utility as utility
import cloudpassage.sanity as sanity
from http_helper import HttpHelper
from cloudpassage.policy import Policy


class FimPolicy(Policy):
    """Initializing the FimPolicy class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    policy = "fim_policy"
    policies = "fim_policies"

    def endpoint(self):
        return("/v1/%s" % FimPolicy.policies)

    def pagination_key(self):
        return(FimPolicy.policies)

    def policy_key(self):
        return(FimPolicy.policy)


class FimBaseline:
    """Initializing the FimBaseline class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    def __init__(self, session):
        self.session = session
        return None

    def list_all(self, fim_policy_id):
        """Returns a list of all baselines for the indicated FIM policy

        Args:
            fim_policy_id (str): ID of fim policy

        Returns:
            list: List of all baselines for the given policy

        """

        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/%s/baselines" % fim_policy_id
        key = "baselines"
        max_pages = 30
        response = request.get_paginated(endpoint, key, max_pages)
        return(response)

    def describe(self, fim_policy_id, fim_baseline_id):
        """Returns the body of the baseline indicated by fim_baseline_id.

        Args
            fim_policy_id (str): ID of FIM policy
            fim_baseline_id (str): ID of baseline

        Returns:
            dict: Dictionary describing FIM baseline

        """

        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/%s/baselines/%s" % (fim_policy_id,
                                                         fim_baseline_id)
        response = request.get(endpoint)
        result = response["baseline"]
        return(result)

    def create(self, fim_policy_id, server_id, **kwargs):
        """Creates a FIM baseline

        Args:
            fim_policy_id (str): ID of FIM policy to baseline
            server_id (str): ID of server to use for generating baseline

        Keyword Args:
            expires (int): Number of days from today for expiration of baseline
            comment (str): Guess.

        Returns:
            str: ID of new baseline

        """

        sanity.validate_object_id([fim_policy_id, server_id])
        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/%s/baselines" % fim_policy_id
        request_body = {"baseline": {"server_id": server_id,
                                     "expires": None,
                                     "comment": None}}
        if "expires" in kwargs:
            request_body["expires"] = kwargs["expires"]
        if "comment" in kwargs:
            request_body["comment"] = kwargs["comment"]
        response = request.post(endpoint, request_body)
        policy_id = response["baseline"]["id"]
        return(policy_id)

    def delete(self, fim_policy_id, fim_baseline_id):
        """Delete a FIM baseline by ID

        Args:
            fim_policy_id (str): ID of FIM policy
            fim_baseline_id (str): ID of baseline to be deleted

        Returns:
            None if successful, exceptions throw otherwise.

        """

        sanity.validate_object_id([fim_policy_id, fim_baseline_id])
        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/%s/baselines/%s" % (fim_policy_id,
                                                         fim_baseline_id)
        response = request.delete(endpoint)
        return(None)

    def update(self, fim_policy_id, fim_baseline_id, server_id):
        """Update a FIM policy baseline.

        Args:
            fim_policy_id (str): ID of fim policy
            fim_baseline_id (str): ID of baseline to be updated
            server_id (str): ID of server to use when generating new baseline

        Returns:
            None if successful, exceptions throw otherwise.

        """

        sanity.validate_object_id([fim_policy_id, fim_baseline_id, server_id])
        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/%s/baselines/%s" % (fim_policy_id,
                                                         fim_baseline_id)
        request_body = {"baseline": {"server_id": server_id}}
        response = request.put(endpoint, request_body)
        return(None)
