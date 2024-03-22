/***************
*
* Autores: Jose Luis Capote, Eduardo Junoy
*
* Grupo: 1131
*
****************/

/***************
* EJERCICIO 4 (2p). Combate Pokémon
*
* Ash, Misty y Brock van a medir sus fuerzas en combates Pokémon. Para ello,
* Ash cuenta con sus amigos Pikachu, Charmander y Bulbasaur, Misty con sus 
* pokémon de tipo agua Psyduck, Staryu y Starmie y Brock con sus criaturas 
* de tipo roca Geodude, Golem y Onyx. Hemos creado el predicado pokemonOfTrainer/2 
* para relacionar cada pokémon con su entrenador. También hemos construido el 
* predicado pokemonOfType/2 que nos indica el tipo de cada pokémon. Por último, 
* hemos creado el predicado typeWins/2 para introducir la tabla de tipos, 
* que nos indica si un pokémon gana a otro en función de su tipo. 
*
****************/

pokemonOfTrainer(pikachu, ash).
pokemonOfTrainer(charmander, ash).
pokemonOfTrainer(bulbasaur, ash).

pokemonOfTrainer(psyduck, misty).
pokemonOfTrainer(staryu, misty).
pokemonOfTrainer(starmie, misty).

pokemonOfTrainer(geodude, brock).
pokemonOfTrainer(golem, brock).
pokemonOfTrainer(onyx, brock).

pokemonOfType(pikachu, electric).
pokemonOfType(charmander, fire).
pokemonOfType(bulbasaur, grass).
pokemonOfType(psyduck, water).
pokemonOfType(staryu, water).
pokemonOfType(starmie, water).
pokemonOfType(geodude, rock).
pokemonOfType(golem, rock).
pokemonOfType(onyx, rock).

typeWins(water, fire).
typeWins(fire, grass).
typeWins(grass, water).
typeWins(water, rock).
typeWins(rock, fire).
typeWins(grass, rock).
typeWins(electric, water).
typeWins(rock, electric).

% 1) Construye el predicado pokemonWins/2 que indique que un pokémon A gana a 
% un pokémon B si el tipo de A gana al tipo de B.
pokemonWins(A, B) :- pokemonOfType(A, TA), pokemonOfType(B, TB), typeWins(TA, TB).

% 2) Construye el predicado trainerWins/2 que nos indique que un entrenador A
% gana a un entrenador B si...
% a) El primer pokémon del entrenador A gana al primero del B, el segundo de A
% gana al segundo de B y el tercero de A gana al tercero de B.
% b) Al menos dos pokémon del entrenador A ganan a sus equivalentes del entrenador B. 
% c) Un pokémon del entrenador A es capaz de ganar a los tres del entrenador B. 

% CASO A: Evalúa la condición de victoria del entrenador A sobre el entrenador B cuando cada uno de los pokémon de A gana a su correspondiente en B.
trainerWinsA(TrA, TrB) :- pokemonOfTrainer(P1A, TrA), pokemonOfTrainer(P1B, TrB), pokemonWins(P1A, P1B),
                         pokemonOfTrainer(P2A, TrA), pokemonOfTrainer(P2B, TrB), pokemonWins(P2A, P2B),
                         pokemonOfTrainer(P3A, TrA), pokemonOfTrainer(P3B, TrB), pokemonWins(P3A, P3B), P1A \= P2A, P1A \= P3A, P2A \= P3A, P1B \= P2B, P1B \= P3B, P2B \= P3B.
% CASO B: Evalúa la condición de victoria del entrenador A sobre el entrenador B cuando al menos dos de los pokémon de A ganan a sus correspondientes en B.
trainerWinsB(TrA, TrB) :- pokemonOfTrainer(P1A, TrA), pokemonOfTrainer(P1B, TrB), pokemonWins(P1A, P1B),
                         pokemonOfTrainer(P2A, TrA), pokemonOfTrainer(P2B, TrB), pokemonWins(P2A, P2B) , P1A \= P2A, P1B \= P2B.

% CASO C: Evalúa la condición de victoria del entrenador A sobre el entrenador B cuando un único pokémon de A es capaz de ganar a los tres pokémon de B.
trainerWinsC(TrA, TrB) :- pokemonOfTrainer(P1A, TrA), pokemonOfTrainer(P1B, TrB), pokemonOfTrainer(P2B, TrB), pokemonOfTrainer(P3B, TrB),
                         pokemonWins(P1A, P1B), pokemonWins(P1A, P2B), pokemonWins(P1A, P3B), P1B \= P2B, P1B \= P3B, P2B \= P3B.
% Verifica todas las condiciones de victoria (casos A, B y C) para determinar si un entrenador A gana a un entrenador B.
trainerWins(TrA, TrB) :- trainerWinsA(TrA, TrB).
trainerWins(TrA, TrB) :- trainerWinsB(TrA, TrB).
trainerWins(TrA, TrB) :- trainerWinsC(TrA, TrB).

% 3) ¿Quién gana los combates Ash vs Misty, Misty vs Brock y Brock vs Ash
% utilizando los criterios a, b y c?

% a) Ash vs Misty -> Ash gana en los casos B y C y no gana en el A

% b) Misty vs Brock -> Misty gana en cualquier caso.

% c) Brock vs Ash -> Brock gana con el caso B y no gana en los casos A y C.
