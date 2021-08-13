#!/usr/bin/env python

"""Tests for `pact_testgen` package."""


from pact_testgen.models import Pact


def test_parse_pactfile(pactfile_dict):
    pact = Pact.parse_obj(pactfile_dict)

    assert len(pact.interactions) == len(pactfile_dict["interactions"])
    assert pact.consumer.name
    assert pact.provider.name
    assert pact.metadata.pactSpecification

    assert len(pact.interactions) > 1
    for interaction in pact.interactions:
        assert interaction.providerStates
        assert interaction.description
        assert interaction.request
        assert interaction.response
