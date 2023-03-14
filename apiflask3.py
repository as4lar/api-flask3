from flask import Flask, render_template, jsonify, abort, request
app=Flask(__name__)
persona={'name':'andrea', 'matricula':'1234'}
tasks=[{'id':1, 'name':'cocinar algo bien sabroso', 'status': False}, {'id':2, 'name':'limpiar la casa', 'status': False} ]
uri='/api/'
#arroba nos dice decorators y no modifican el codigo, dependen del decorador
#ayudan a interpretar partes de codigos
#route->ruta de todas las paginas, el index 
#transformar la funcion para que devuelva 
@app.route("/")
def hello_world():
    return render_template("index.html", data=persona)

#API
@app.route(uri+'/tasks', methods=['GET'])
def getTasks():
    return jsonify({'tasks':tasks})

#endpoints->tasks/id 
#metodo->SET, GET
#GET son los que nos devuelven información, no consultamos nada
#POST-> formularios create
"""

-----METODOS HTTP----
C->POST
R->GET
U->PUT
D->DELETE

"""
@app.route(uri+'/tasks/<int:id>', methods=['GET'])
def get_task(id):
    this_task=0
    for task in tasks:
        if task['id']==id:
            this_task=task
    if this_task==0:
        abort(404)
    return jsonify({'task':this_task})


#METODO POST
@app.route(uri+'/tasks', methods=['POST'])
def create_tasks():
    if request.json:
        task={
            'id':len(tasks)+1,
            #accedemos a la llave name
            'name': request.json('name'),
            'status':False
        }
        #añadimos la tarea 201->exito en la operacion
        tasks.append(task)
        return jsonify({'tasks'}), 201
    else:
        abort(404)

#METODO PUT
@app.route(uri+'/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    if request.json:
        #this task va a tener una lista, una lista tiene elementos por posicion
            #en el primer for se utiliza porque no importa el indice, de la lista task toma cada
            #elemento y la vacia en la variable task y en cada iteracion se pregunta si el id 
            #es el que se busca
        this_task=[task for task in tasks if task['id']==id]
        if this_task:
            if request.json.get('name'):
                this_task[0]['name']=request.json('name')

            if request.json.get('status'):
                this_task[0]['status']=request.json('status')

            return jsonify({'task': this_task[0]}), 201
        else:
            abort(404)
    else:
        abort(404)

# METODO DELTE
@app.route(uri+'/tasks/<int:id>', methods=['DELETE'])
def delete_task():
    this_task=[task for task in tasks if task['id']==id]
    if this_task:
        tasks.remove(this_task[0])
        return jsonify({'tasks': tasks})
    else:
        abort(404)

if __name__=='__main__':
    app.run(debug=True)
