from pact_testgen.generator import generate_tests
from pact_testgen.dialects.django import Dialect


def test_django_test_generator_output_is_parsable(testfile):
    test_file, _ = generate_tests(testfile, Dialect())
    compile(test_file, "<string>", "exec")


def test_output_includes_expected_test_cases(testfile):
    test_file, _ = generate_tests(testfile, Dialect())
    # Names of test cases we expect to see. This is driven directly
    # by test_app/client_tests.py
    print(f"\nTEST FILE\n------\n\n{test_file}\n")
    assert "TestAnAuthorWithId1Exists" in test_file
    assert "TestAnAuthorWithId1ExistsABookExistsWithAuthorId1" in test_file
    assert "TestNothing" in test_file


def test_provider_state_file_has_expected_methods(testfile):
    _, provider_state_file = generate_tests(testfile, Dialect())
    print(f"\nPROVIDER STATE FILE\n-------------------\n\n{provider_state_file}\n")
    assert "setup_nothing" in provider_state_file
    assert "setup_an_author_with_id_1_exists" in provider_state_file
    assert (
        "setup_an_author_with_id_1_exists_a_book_exists_with_author_id_1"
        in provider_state_file
    )
