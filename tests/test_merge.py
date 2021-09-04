import sys
from textwrap import dedent

import pytest

from pact_testgen.files import merge


@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9")
def test_merge_empty_target():
    source = dedent(
        """
        def foo():
            pass
    """
    )

    result = merge("", source)

    assert result == dedent(
        """
        def foo():
            pass

        """
    )


@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9")
def test_merge_no_duplicate_functions():
    target = dedent(
        """
        def foo():
            pass

        """
    )

    source = dedent(
        """
        def bar():
            pass
        """
    )

    result = merge(target, source)

    assert result == dedent(
        """
        def foo():
            pass


        def bar():
            pass

        """
    )


@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9")
def test_merge_with_duplicates():
    target = dedent(
        """
        def foo():
            # foo implementation
            pass

        """
    )

    source = dedent(
        """
        def foo():
            raise NotImplementedError()
        """
    )

    result = merge(target, source)

    assert result == dedent(
        """
        def foo():
            # foo implementation
            pass

        """
    )


@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9")
def test_merge_with_duplicate_and_new_function():
    target = dedent(
        """
        def foo():
            # foo implementation
            pass

        """
    )

    source = dedent(
        """
        def foo():
            raise NotImplementedError()


        def bar():
            raise NotImplementedError()

        """
    )

    result = merge(target, source)

    assert result == dedent(
        """
        def foo():
            # foo implementation
            pass


        def bar():
            raise NotImplementedError()

        """
    )
