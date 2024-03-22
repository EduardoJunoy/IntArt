/***************
*
* Autores: Jose Luis Capote, Eduardo Junoy
*
* Grupo: 1131
*
****************/

/***************
* EJERCICIO 3 (2p). Cluedo
*
* Alguien ha cometido un terrible asesinato en la mansión. Hemos podido
* reunir algunas pruebas y pistas sobre los diferentes habitantes de la casa,
* los lugares en los que han estado y las posibles armas que han portado.
* Esto es posible gracias a los predicados fact\3, que relaciona a una persona
* con un lugar y una hora, y hint\3, que relaciona a una persona con un arma
* y una hora. 
*
****************/

fact(amapola, salon, 10).
fact(amapola, cocina, 12).
fact(amapola, comedor, 14).

fact(rubio, billar, 10).
fact(rubio, biblioteca, 12).

fact(blanco, cocina, 12).

fact(prado, biblioteca, 9).

fact(celeste, billar, 11).
fact(celeste, escaleras, 13).

fact(mora, biblioteca, 10).
fact(mora, terraza, 12).

hint(amapola, cuchillo, 10).
hint(amapola, tuberia, 12).

hint(rubio, cuchillo, 10).
hint(rubio, tuberia, 10).
hint(rubio, pistola, 9).

hint(blanco, cuchillo, 13).

hint(prado, cuchillo, 10).

hint(celeste, candelabro, 10).
hint(celeste, tuberia, 11).

hint(mora, pistola, 11).

% 1) Crea un método suspect\3 que devuelva true si la persona X estuvo 
% en la habitación H y empuñó el arma A. Utilízalo para averiguar
% los sospechosos de un crimen cometido en la biblioteca con el cuchillo.

suspect(X, H, A) :- fact(X, H, _), hint(X, A, _).
% esto comprueba que x estuvo en la habitacion H (fact(x,h,_)) y empuño el arma A(hint(x,a,_))
% si lo ejecutamos para el crimen cometido en la biblioteca con el cuchillo, nos devuelve que nadie cumple estos requisitos

% 2) Crea un método guilty\4 para obtener la persona X entre los sospechosos
% que es más probable que cometiera el crimen en la habitación H, usando
% el arma A y a la hora T. Utilízalo para averiguar el culpable del crimen
% cometido en la biblioteca con el cuchillo a las 10.

% comprobamos que X sea sospechoso viendo si cumple las tres condiciones (hora, arma y lugar)
guilty(X, H, A, T) :- suspect(X, H, A), fact(X, H, T), hint(X, A, T).
% como el metodo guilty da false en este caso, buscamos ahora a los que cumplan dos de tres condiciones
% arma y lugar
guilty(X, H, A, T) :- suspect(X, H, A), fact(X, H, T).
% arma y hora
guilty(X, H, A, T) :- suspect(X, H, A), hint(X, A, T).
% lugar y hora
guilty(X, H, A, T) :- fact(X, H, T), hint(X, A, T).

% ejecutando esto, deducimos que hay dos posibles culpables, rubio y prado, que son los unicos que cumplen dos de las tres condiciones
% vease que la ambiguedad se genera porque en este caso no hay nadie que cumpla el metodo suspect