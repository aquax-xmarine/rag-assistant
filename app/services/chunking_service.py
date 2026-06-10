import re


class ChunkingService:

    @staticmethod
    def fixed_chunking(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> list[str]:

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            chunks.append(
                text[start:end]
            )

            start += chunk_size - overlap

        return chunks

    @staticmethod
    def sentence_chunking(
        text: str,
        max_chunk_size: int = 500
    ) -> list[str]:

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        chunks = []
        current_chunk = ""

        for sentence in sentences:

            if (
                len(current_chunk)
                + len(sentence)
                <= max_chunk_size
            ):
                current_chunk += (
                    sentence + " "
                )

            else:
                chunks.append(
                    current_chunk.strip()
                )

                current_chunk = (
                    sentence + " "
                )

        if current_chunk:
            chunks.append(
                current_chunk.strip()
            )

        return chunks