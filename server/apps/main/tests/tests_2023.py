import vcr
import urllib.request
import json


@vcr.use_cassette("server/apps/main/tests/fixtures/share_experience.yaml")
def test_share_experience():
    """
    Check the details and warnings are as expected
    """
    r = (
        urllib.request.urlopen(
            "https://www.openhumans.org/api/direct-sharing/project/exchange-member/"
        )
        .read()
        .decode()
    )
    response = json.loads(r)["data"][0]["metadata"]["data"]

    assert response["title_text"] == "Story the first"
    assert (
        "However little known the feelings or views of such a man"
        in response["difference_text"]
    )
    assert "It is a truth universally acknowledged" in response["experience_text"]
    assert [
        response["drug"],
        response["abuse"],
        response["other"],
        response["negbody"],
        response["violence"],
        response["mentalhealth"],
    ] == [False, False, "", False, False, False]

    assert [response["research"], response['viewable']] == [True, True]
