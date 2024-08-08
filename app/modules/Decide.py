class decide: 
    
    def decision (self, question):

        if question=="1.- el cliente esta saludando":
            contexto = """ solo necesita que saludes esta vez, presentate de manera cordial y ofrece ayuda
                            Ej: ¡Hola! Bienvenido al servicio de atención automatica de Col Network. Soy SOF.IA, tu asistente virtual no humano. ¿En qué puedo ayudarte hoy?"""
            return contexto
        
        elif question== "2.-su consulta es referente a planes":
            contexto = """                Planes de Internet:

                -Plan 300 Mbps:
                Velocidad: 300 Mbps
                Precio: $20
                Anteriormente: 100 Mbps

                -Plan 600 Mbps:
                Velocidad: 600 Mbps
                Precio: $25
                Anteriormente: 300 Mbps

                -Plan 1 Gbps:
                Velocidad: 1 Gbps
                Precio: $30
                Anteriormente: 600 Mbps
                Incluye: 1 Router
                                 
                Contexto adicional si alguien quiere cambiar su plan: debes revisar si ya le mostraste nuestros planes, en caso de que  no lo hayas hecho debes mostrar las opciones disponibles y redirigirlo con el contacto de soporte, si ya lo hiciste puedes redirigir siempre explicando que ese contacto va a ayudarlo con su peticion"""
            return contexto
        else: 
            return "no entendiste esta consulta porque sale de tus posibilidades como asistente virtual, por tanto debes pedir mas contexto a la misma"
