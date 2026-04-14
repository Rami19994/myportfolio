from pathlib import Path
from asgiref.sync import async_to_sync
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from vercel.blob import AsyncBlobClient


@deconstructible
class VercelBlobStorage(Storage):
    def _save(self, name, content):
        content.seek(0)
        file_bytes = content.read()
        pathname = Path(name).as_posix()

        blob = async_to_sync(self._put_blob)(pathname, file_bytes)

        # نخزن الرابط النهائي مباشرة في الحقل
        return blob.url

    async def _put_blob(self, pathname: str, file_bytes: bytes):
        client = AsyncBlobClient()
        return await client.put(
            pathname,
            file_bytes,
            access="public",
            add_random_suffix=True,
        )

    def exists(self, name):
        return False

    def url(self, name):
        # بما أننا نخزن URL كامل في قاعدة البيانات
        return name

    def delete(self, name):
        # ممكن نضيف حذف لاحقًا إذا احتجته
        pass
