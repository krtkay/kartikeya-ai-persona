from langchain_text_splitters import RecursiveCharacterTextSplitter


class ResumeChunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=150
        )

    def chunk_text(self, text):

        return self.splitter.split_text(text)
    
    def chunk_document(self,text):

        return self.splitter.split_text(
            text
        )