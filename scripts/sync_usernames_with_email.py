from django.contrib.auth import get_user_model

User = get_user_model()

fixed = 0
skipped = 0

for user in User.objects.all().order_by("id"):
    email = (user.email or "").strip().lower()
    if not email:
        skipped += 1
        continue

    conflict = User.objects.filter(username=email).exclude(pk=user.pk).exists()
    if conflict:
        skipped += 1
        continue

    if user.username != email:
        user.username = email
        user.save(update_fields=["username"])
        fixed += 1

summary = {}
for user in User.objects.all():
    key = getattr(user, "user_type", "unknown")
    summary[key] = summary.get(key, 0) + 1

print("sync complete")
print("fixed=", fixed)
print("skipped=", skipped)
print("summary=", summary)
