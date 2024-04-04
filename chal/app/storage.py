from django.contrib.messages.storage.base import BaseStorage

class CustomMessageStorage(BaseStorage):
    def get_signed_cookie(self, request, key, default=None):
        if key == 'signer_key':
            # Block access to the secret key
            return None  # or raise an exception
        else:
            # For other keys, use the default behavior
            return super().get_signed_cookie(request, key, default)
