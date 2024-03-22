/***************
*
* Autores: Jose Luis Capote, Eduardo Junoy
*
* Grupo: 1131
*
****************/

/***************
* EJERCICIO 5 (2p). Procesamiento de sentencias
*
* Si bien un procesamiento completo de lenguaje es una tarea compleja, debido a que
* su uso no siempre es estructurado, podemos utilizar, a base de reglas sencillas, Prolog
* para identificar "frases bien formadas".
* Para ello, se os da una base de conocimiento inicial y se os pide que diseñéis un predicado
* que identifique si una frase es correcta. En el resto del ejercicio iréis ampliando las 
* reglas para identificar frases cada vez más complejas.
*
****************/

% Partimos de la siguiente base de conocimiento simplificada
articulo([X]) :- articulo(X).
articulo(el).
articulo(la).
articulo(un).
articulo(una).

nombre([X]) :- nombre(X).
nombre(perro).
nombre(hueso).
nombre(gato).
nombre(parque).


verbo([X]) :- verbo(X).
verbo(come).
verbo(encuentra).
verbo(pasea).
verbo(juega).
verbo(corre).

adjetivo([X]) :- adjetivo(X).
adjetivo(hermoso).
adjetivo(blanco).
adjetivo(grande).
adjetivo(bonito).
adjetivo(delicioso).

% 1. Define un predicado frase/1 que determine si una frase 
% (codificada como una lista de terminales) es correcta gramaticalmente.
% De momento, nos basta con identificar frases como la siguiente, donde hay un sintagma nominal
% y uno verbal, pero sin complemento de ningún tipo:
% :- frase([el, perro, come]).
% :- frase([la, perro, come]).
% Sin embargo, la siguiente fallaría:
% :- frase([come]). FAIL
% El predicado append/3 puede ser útil para asignar partes de una frase a variables.

% Este método define un sintagma nominal con su corresponiente artículo y nombre.
sintagma_nominal([Art, Nom]):-
    articulo([Art]),
    nombre([Nom]).
% Este método define un sintagma verbal con su corresponiente verbo.
sintagma_verbal([Verb]) :-
    verbo([Verb]).
% Este método define una frase compuesta de un sintagma nominal y un sintagma verbal.
frase(F):-
    append(N, V, F),
    sintagma_nominal(N),
    sintagma_verbal(V).

%Comprobamos que funciona para los ejemplos mostrados y efectivamente:
%Para la consulta frase([el, perro, come]). devuelve True.
%Para la consulta frase([la, perro, come]). devuelve True.
%Para la consulta frase([come]). devuelve False.

% 2. Amplía la base de conocimiento con más hechos (nombres, verbos, determinantes). 
% Al igual que en el ejercicio anterior, no nos vamos a preocupar de la concordancia de género.
% Extiende el predicado anterior y llámalo frase2/1 para que reconozca frases 
% cuyo sintagma verbal tenga uno (o varios) complementos.
% Puedes reutilizar todos los predicados que consideres, pero si tienes que cambiar alguno, 
% renómbralo para mantener la compatibilidad con los ejercicios anteriores.

% Este método define un sintagma verbal ampliado con uno o varios complementos
sintagma_verbal_ampliado([Verb|Comp]):-
    (verbo([Verb]), nombre(Comp));             %El complemento es un nombre
    (verbo([Verb]), sintagma_nominal(Comp));   %El complemento es un sintagma nominal
    sintagma_verbal([Verb|Comp]).

% Este método define una frase compuesta de un sintagma nominal y un sintagma verbal ampliado.
frase2(F):-
    append(N, V, F),
    sintagma_nominal(N),
    sintagma_verbal_ampliado(V).

%Comprobamos su correcto funcionamiento con algunas consultas como:
%frase2([el, perro, come, hueso]). devuelve True
%frase2([el, perro, come, un, hueso]). devuelve True
%frase2([el, perro, pasea, un, parque]). devuelve True
%frase2([pasea, un, parque]). devuelve False

% 3. Añade adjetivos a la base de conocimiento y crea el predicado frase3/1 que detecte si 
% un nombre va acompañado de un adjetivo. Es decir:
% :- frase3([el, perro, grande, come]).
% De manera opcional, permite la utilización de adjetivos tanto delante como detrás del nombre.

% Define otro sintagma nominal con las distintas combinaciones de artículo, nombre y adjetivo.
sintagma_nominal_ampliado([Art, Adj, Nom]) :-
    articulo(Art),
    adjetivo(Adj),
    nombre(Nom).
sintagma_nominal_ampliado([Art, Nom, Adj]) :-
    articulo(Art),
    nombre(Nom),
    adjetivo(Adj).
% Este método define una frase compuesta de un sintagma nominal ampliado y un sintagma verbal ampliado.
frase3(Frase):-
    append(N, V, Frase),
    sintagma_nominal_ampliado(N),
    sintagma_verbal_ampliado(V).

%Estas nuevas formas de construir las frases nos dan mayor versatilidad para consultas como:
%frase3([el, perro, hermoso, come, hueso]). devuelve True
%frase3([el, hermoso, perro, come, hueso]). devuelve True
%frase3([perro, hermoso, come, hueso]). devuelve False


% 4. Identifica un ejemplo de frase que no lo detecte alguno de tus predicados y explica 
% cuál sería el motivo. Puedes utilizar la lectura declarativa o procedural 
% vista en el ejercicio 1 o apoyarte en trace/0 para tu explicación.

% "El perro blanco y el gato pardo" Esta frase no sería detectada por el uso de conjunciones como, en este caso, "y".
% "Los perros pasean" Esta frase no sería reconocida porque no se contempla el plural, en este caso "Los perros".
% "El perro hermoso pasea con su dueño" Esta frase no sería reconocida por el uso de preposiciones como, en esta ocasión "con".
% "El perro que juega es bonito" Esta frase no sería detectada por el uso de subordinadas. En este caso "que juega".