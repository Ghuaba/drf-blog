#Para obtener una ip unica para cada usuario, si no existe tomammos la primero por defecto
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]#TOmamos la primera ip real del cliente, por si pasa por proxies, separadas por comas
    else:
        ip = request.META.get('REMOTE_ADDR')# es la IP directamente reportada por el socket TCP (puede ser la del proxy si hay uno en medio)
    
    return ip

def get_post_uuid(post):
    """
    Devuelve el UUID del post como string,
    sin importar si viene de la DB (objeto) o del cache (dict).
    """
    if isinstance(post, dict):
        return post["uuid"]
    return str(post.uuid)
