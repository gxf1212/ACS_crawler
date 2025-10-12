Contributing
============

We welcome contributions! This guide will help you get started.

Development Setup
-----------------

1. Fork the repository on GitHub: https://github.com/gxf1212/ACS_crawler
2. Clone your fork::

    git clone https://github.com/YOUR-USERNAME/ACS_crawler.git
    cd ACS_crawler

3. Create conda environment::

    conda create -n acs_crawler python=3.9
    conda activate acs_crawler

4. Install dependencies::

    pip install -r requirements.txt

5. Create a feature branch::

    git checkout -b feature/your-feature-name

Code Style
----------

* Follow PEP 8
* Use type hints
* Write Google-style docstrings
* Keep functions small and focused

Example::

    def get_paper_metadata(url: str) -> Optional[PaperMetadata]:
        """Get metadata from paper URL.

        Args:
            url: Paper URL

        Returns:
            PaperMetadata object or None if failed

        Raises:
            ValueError: If URL is invalid
        """
        pass

Testing
-------

1. Write tests for new features
2. Run tests::

    pytest tests/

3. Check coverage::

    pytest --cov=acs_crawler tests/

Documentation
-------------

* Update relevant .rst files in ``docs/``
* Build docs locally::

    cd docs
    make html

* Check output in ``docs/_build/html/``

Pull Request Process
--------------------

1. Ensure tests pass
2. Update documentation
3. Commit with clear message::

    git commit -m "Add: Brief description of changes"

4. Push to your fork::

    git push origin feature/your-feature-name

5. Create Pull Request on GitHub
6. Describe your changes clearly
7. Link related issues

Commit Message Format
---------------------

Use conventional commits::

    type(scope): description

    [optional body]

    [optional footer]

Types:

* **feat**: New feature
* **fix**: Bug fix
* **docs**: Documentation
* **style**: Formatting
* **refactor**: Code restructuring
* **test**: Adding tests
* **chore**: Maintenance

Example::

    feat(api): add CSV export endpoint

    - Implemented /api/papers/export/csv
    - Returns papers in CSV format
    - Includes all metadata fields

    Closes #123

Code Review
-----------

* Be respectful and constructive
* Focus on code quality
* Explain your suggestions
* Be open to feedback

Questions?
----------

* Open an issue for bugs
* Start a discussion for questions
* Check existing issues first
