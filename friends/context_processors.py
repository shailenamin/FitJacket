from .models import WorkoutGroup, GroupMember

def user_groups(request):
    if request.user.is_authenticated:
        groups = WorkoutGroup.objects.filter(groupmember__user=request.user)
    else:
        groups = []
    return {'user_groups': groups}