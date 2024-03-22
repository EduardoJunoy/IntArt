/***************
*
* Autores: Jose Luis Capote, Eduardo Junoy
*
* Grupo: 1131
*
****************/

/***************
* EJERCICIO 2 (2p). Casa Stark
*
* Construir un árbol genealógico con Prolog es fácil. Basta con crear 
* un predicado parent\2 para indicar que una persona es padre o madre de otra 
* y así construir de generación en generación. Aquí hemos creado 
* la casa Stark de Juego de tronos. 
*
****************/

parent(eddard, robb).
parent(eddard, bran).
parent(eddard, rickon).
parent(eddard, sansa).
parent(eddard, arya).
parent(catelyn, robb).
parent(catelyn, bran).
parent(catelyn, rickon).
parent(catelyn, sansa).
parent(catelyn, arya).

parent(rickard, eddard).
parent(rickard, brandon).
parent(rickard, benjen).
parent(rickard, lyanna).
parent(lyarra, eddard).
parent(lyarra, brandon).
parent(lyarra, benjen).
parent(lyarra, lyanna).

male(rickard).
male(brandon).
male(eddard).
male(benjen).
male(robb).
male(bran).
male(rickon).

female(lyarra).
female(lyanna).
female(catelyn).
female(sansa).
female(arya).

% 1) Empleando el predicado parent, construye los siguientes métodos:
% father(M, N), que devuelva True si M es el padre de N.
% mother(M, N), que devuelva True si M es la madre de N.
% son(M, N), que devuelva True si M es el hijo de N.
% daugther(M, N), que devuelva True si M es la hija de N.

% es padre si es hombre y es padre
father(M, N) :- male(M), parent(M, N).
% es madre si es mujer y es madre
mother(M, N) :- female(M), parent(M, N).
% m es hijo de n si n es padre de m y m es hombre
son(M, N) :- parent(N, M), male(M).
% m es hija de n si n es padre de m y m es mujer
daugther(M, N) :- parent(N, M), female(M).


% 2) Construye los métodos grandparent, grandfather y grandmother 
% que permitan encontrar los abuelos de un Stark, así como los métodos
% grandson y grandaugther que devuelvan los nietos y nietas de un Stark.

% m es abuelo de n si m es padre de x y x es padre de n
grandparent(M, N) :- parent(M, X), parent(X, N).
% m es abuelo de n si m es abuelo de x y x es padre de n y m es hombre
grandfather(M, N) :- grandparent(M, N), male(M).
% m es abuela de n si m es abuela de x y x es padre de n y m es mujer
grandmother(M,N) :- grandparent(M, N), female(M).


% 3) ¿Cómo crearías los métodos de hermano (brother), hermana (sister),
% tío (uncle), tía (aunt), sobrino (nephew) y sobrina (niece).

%  se asume que hermano/hermana solo se cumple si comparten tanto padre como madre
%  ya que sino se repiten los hermanos

% m es hermano de n si m y n tienen el mismo padre y la misma madre y m es hombre y m no es n
brother(M, N) :- father(X, M), father(X, N), mother(Y, M), mother(Y, N), male(M), M \= N.
% m es hermana de n si m y n tienen el mismo padre y la misma madre y m es mujer y m no es n1
sister(M, N) :- father(X, M), father(X, N), mother(Y, M), mother(Y, N), female(M), M \= N.

% m es tio de n si m es hermano de x y x es padre de n
uncle(M, N) :- parent(X, N), brother(M, X).

% m es tia de n si m es hermana de x y x es padre de n
aunt(M, N) :- parent(X, N), sister(M, X).

% m es sobrino de n si m es hijo de x y x es hermano o hermana de n y m es hombre
nephew(M, N) :- parent(X, M), brother(X, N), male(M).
nephew(M, N) :- parent(X, M), sister(X, N), male(M).
% m es sobrina de n si m es hijo de x y x es hermano o hermana de n y m es mujer
niece(M, N) :- parent(X, M), sister(X, N), female(M).
niece(M, N) :- parent(X, M), brother(X, N), female(M).