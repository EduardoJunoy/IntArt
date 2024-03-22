/***************
*
* Autores: Jose Luis Capote, Eduardo Junoy
*
* Grupo: 1131
*
****************/

/***************
* Introducción
*
* Os recomendamos echar un vistazo a la colección de 99 problemas de Prolog publicados en 
* https://www.ic.unicamp.br/~meidanis/courses/mc336/2009s2/prolog/problemas/
* Ahí puedes encontrar una gran serie de problemas con código que te pueden ayudar 
* como entrenamiento.
*
****************/

/***************
* Entrega
*
* Se debe entregar un único fichero comprimido cuyo nombre, todo él en minúsculas y sin acentos, 
* tildes, o caracteres especiales, tendrá la siguiente estructura:
*       p3_gggg_mm_apellido1_apellido2.zip
* Donde gggg es el identificador del grupo y mm es el de la pareja.
* Este fichero debe incluir los ficheros .pl entregados por los profesores con sus correspondientes
* soluciones y descripciones de las mismas como comentarios (no hace falta entregar una memoria por separado).
*
* Recordad utilizar nombres informativos para los términos (hechos, reglas) así como comentar vuestro código 
* adecuadamente para que resulte de fácil lectura.
*
****************/


/***************
* EJERCICIO 1 (1p). Ejercicio de lectura
*
* Escribe la lectura declarativa (para el caso general) 
* y procedural (para la consulta slice([1, 2, 3, 4], 2, 3, L2))
* del predicado slice/4, disponible en
* https://www.ic.unicamp.br/~meidanis/courses/mc336/2009s2/prolog/problemas/p18.pl
*
* Véase https://www.metalevel.at/prolog/reading para un ejemplo.
*
****************/

/*
* Lectura Declarativa:
* 1. La primera cláusula toma una lista "[X|_]", unos índices de inicio y final "1" y devuelve una nueva lista "[X]", que es el primer y único elemento de la lista.
* 2. Si se puede extraer una sublista "Ys" de la cola "Xs" de una lista, empezando desde el índice "1" y terminando en "K1", donde "K1" es "K - 1", entonces se puede formar una sublista "[X|Ys]" a partir de la lista completa "[X|Xs]" comenzando desde el índice "1" y terminando en "K"
* 3. Si se puede extraer una sublista "Ys" de la cola "Xs" de una lista, empezando desde el índice "I1", donde "I1" es "I - 1", y terminando en "K1", donde "K1" es "K - 1", entonces esa misma sublista "Ys" es también la sublista de la lista original que empieza en el índice "I" y termina en "K". 
*/

/*
* Lectura Procedural:
* 1. ¿Se aplica la primera cláusula? No, porque los índices "I" y "K" no son igual a "1", sino que son "2" y "3", respectivamente.
* 2. ¿Se aplica la segunda cláusula? No, porque el índice "I" no es igual a "1", sino que es "2".
* 3. ¿Se aplica la tercera cláusula? Sí, ya que el contenido de "Xs" es "[2, 3, 4]", "I" es "2", "I1" es "1", "K" es "3", "K1" es "2" y "Ys" es "L2". 
* 4. Se realiza la siguiente llamada con slice([2, 3, 4], 1, 2, L2).
* 5. ¿Se aplica la primera cláusula? No, porque los índices "I" y "K" no son igual a "1" ambos, sino que son "1" y "2", respectivamente.
* 6. ¿Se aplica la segunda cláusula? Sí, la segunda cláusula aplica con "X" siendo el elemento "2", "Xs" contiene "[3, 4]", "K" es "2", "K1" es "1" y "L2" es "[X|L2]"
* 7. Se realiza la siguiente llamada con slice([3, 4], 1, 1, L2).
* 8. ¿Se aplica la primera cláusula? Sí, ya que los índices "I" y "K" son igual a "1". Al cumplirse el caso base, el resultado de "L2" y, por tanto, de "Ys" es "[3,4]". Se comprueba si se cumplen el resto de cláusulas.
* 9. ¿Se aplica la segunda cláusula? No, porque no se cumple la condición "K>1".
* 10.¿Se aplica la tercera cláusula? No, porque no se cumplen las condiciones "I>1" ni "K>1".
*
*/

