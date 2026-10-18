from .models import LibraryRegistration

def register_library(
    library_name: str,
    module_path: str,
    class_name: str,
    description: str = "",
):
    # Keyed as the model's unique_together, so registering again updates instead of failing.
    registration, _ = LibraryRegistration.objects.update_or_create(
        module_path=module_path,
        class_name=class_name,
        defaults={"library_name": library_name, "description": description},
    )
    return registration
