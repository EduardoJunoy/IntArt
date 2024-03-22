/***************
*
* Autores: Jose Luis Capote, Eduardo Junoy
*
* Grupo: 1131
*
****************/

/***************
* EJERCICIO 6 (1p). Librería clpb
*
* La librería CLP(B) (ver https://www.swi-prolog.org/pldoc/man?section=clpb)
* permite resolver problemas combinatorios con restricciones.
*
* A continuación se os da la solución al siguiente problema resuelto con esta librería:
* Tenemos a 3 sospechosos de un robo, Alice (A), Bob (B) y Carl (C). 
* Al menos uno de ellos es culpable. Condiciones:
* Si A es culpable, tiene exactamente 1 cómplice.
* Si B es culpable, tiene exactamente 2 cómplices.
* ¿Quién es culpable?
*
****************/

:- use_module(library(clpb)).

solve(A,B,C) :-
% Hay al menos un culpable
sat(A + B + C),
% Si A es culpable, tiene exactamente 1 cómplice.
sat(A =< B # C),
% Si B es culpable, tiene exactamente 2 cómplices.
sat(B =< A * C),
% Asigna valores a las variables de manera que se satisfagan todas las restricciones.
labeling([A,B,C]).


% 1. Plantea una solución a este problema que sea equivalente a la encontrada por la librería.
% Asegura que al menos uno entre A, B, y C es culpable, es decir, verdadero.
un_culpable_o_mas(1, _, _).
un_culpable_o_mas(_, 1, _).
un_culpable_o_mas(_, _, 1).

% Si A es verdadero, entonces exactamente uno entre B y C son cómplices, es decir, son verdaderos.
a_tiene_un_complice(1, B, C) :- B + C =:= 1.
a_tiene_un_complice(0, _, _).

% Si B es verdadero, entonces ambos A y C son verdaderos.
b_tiene_dos_complices(1, A, C) :- A + C =:= 2.
b_tiene_dos_complices(0, _, _).

% Solución que satisface el problema.
solucion(A, B, C) :-
    member(A, [0, 1]), %Explora las combinaciones posibles con A = 0 y A = 1
    member(B, [0, 1]), %Explora las combinaciones posibles con B = 0 y B = 1
    member(C, [0, 1]), %Explora las combinaciones posibles con C = 0 y C = 1
    un_culpable_o_mas(A, B, C),
    a_tiene_un_complice(A, B, C),
    b_tiene_dos_complices(B, A, C).

% Para la ejecución de solve(A, B, C) se obtiene:
% A = B, B = 0, C = 1
% A = C, C = 1, B = 0
%
% Sin, embargo para solucion(A, B, C):
% A = B, B = 0, C = 1
% A = C, C = 1, B = 0
% A = C, C = 1, B = 0 %Se repite la segunda solución por falta de backtracking y optimizaciones
%
% Esta diferencia entre la programacion manual y la de la librería seguramente se deba al backtracking 
% (la técnica algoritmica utilizada para hallar soluciones a problemas) y las posibles optimizaciones
% internas de la librería que pueden influir en cómo se encuentran las soluciones.

% 2. Discute las ventajas e inconvenientes entre la solución encontrada y el uso de la librería.

% Las ventajas de la solución encontrada son, que por un lado no se depende de ninguna librería externa, lo que hace esta solución más versátil y flexible, y por otro que 
% la solución manual ofrece mayor control sobre la lógica, lo que elimina ineficiencias en los procesos.
%
% Las desventajas son, que debido a la definición manual hay mayor riesgo de errores e implican mayor tiempo en su elaboración, y que quizás no encontremos la solución
% óptima respecto a una librería especializada como CLP(B), es decir, aumenta la complejidad en su conjunto.
% En este caso se ve claramente cómo la solución manual no es óptima y la de la librería sí porque da menor número de soluciones para optimizar la respuesta.
% Además, también se observa la diferencia de complejidad; lo que con la librería son 5 líneas de código, manualmente son 15.
