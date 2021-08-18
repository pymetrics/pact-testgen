from pact_testgen.generators.django.generator import generate_tests


def test_django_test_generator_output_is_parsable(testfile):
    output = generate_tests(testfile)
    code_obj = compile(output, "<string>", "exec")
    # Names of test cases we expect to see. This is driven directly
    # by test_app/client_tests.py
    assert "TestAnAuthorWithId1Exists" in code_obj.co_names
    assert "TestABookExistsWithAuthorId1AnAuthorWithId1Exists" in code_obj.co_names
    assert "TestNothing" in code_obj.names
