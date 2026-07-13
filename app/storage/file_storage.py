from pathlib import Path
import uuid

from fastapi import UploadFile


class FileStorage:

    BASE_PATH = Path("uploads")

    @classmethod
    async def save_files(
        cls,
        check_id: uuid.UUID,
        files: list[UploadFile],
    ) -> list[dict]:

        check_directory = cls.BASE_PATH / str(check_id)

        check_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        saved_files = []

        for file in files:
            safe_name = Path(file.filename).name
            file_path = check_directory / safe_name

            content = await file.read()

            with open(
                file_path,
                "wb"
            ) as buffer:
                buffer.write(content)

            saved_files.append(
                {
                    "filename": file.filename,
                    "file_path": str(file_path),
                    "size": len(content),
                    "content_type": file.content_type,
                }
            )

        return saved_files