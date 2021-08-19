from pact_testgen.generators.django.generator import generate_tests


def test_django_test_generator_output_is_parsable(testfile):
    output = generate_tests(testfile)
    compile(output, "<string>", "exec")


def test_output_includes_expected_test_cases(testfile):
    output = generate_tests(testfile)
    # Names of test cases we expect to see. This is driven directly
    # by test_app/client_tests.py
    print(f"\nOUTPUT\n------\n\n{output}\n")
    assert "TestAnAuthorWithId1Exists" in output
    assert "TestAnAuthorWithId1ExistsABookExistsWithAuthorId1" in output
    assert "TestNothing" in output
