class MetaData:
    def __init__(self, response):
        self.get_response = response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            message = f'Olá,{request.user.username}! Bom dia!'
        else:
            message = 'Olá, bom dia!'
        request.session['message'] = message
        return None