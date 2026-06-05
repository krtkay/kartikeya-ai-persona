class DocumentBuilder:

    @staticmethod
    def resume_document(
        text,
        section
    ):

        return {
            "text": text,
            "metadata": {
                "source": "resume",
                "section": section,
                "document_type": "resume"
            }
        }

    @staticmethod
    def readme_document(
        text,
        repo
    ):

        return {
            "text": text,
            "metadata": {
                "source": "github",
                "repo": repo,
                "document_type": "readme"
            }
        }

    @staticmethod
    def commit_document(
        text,
        repo
    ):

        return {
            "text": text,
            "metadata": {
                "source": "github",
                "repo": repo,
                "document_type": "commit"
            }
        }