## Ce document sert à voir quelles choses à faire sont possibles, et ce ne sont que des propositions. Il y a des propositions de fixs, d'implémentations...
### Les TODO ne sont pas dans l'ordre dans lequel il faut les faire, ils sont juste organisés selon le moment où j'y ai pensé :)

Chaque TODO à 3 états :
- [ ] -> non fait
- [?] -> fait mais avec quelques différences ou quelques subtilités
- [x] -> fait

1. #### [x] TODO #1: 
* cases en 64x64
2. #### [x] TODO #2: 
* essayer d'utiliser delta ?
> pour l'instant seulement utilisé avec `CAMERA_SPEED`, donc j'ai ajouté un **TODO** bonus pour ne pas oublier de l'utiliser ailleurs
3. #### [x] TODO #3: 
* pouvoir changer taille tiles (`TILE_SIZE`) sans bugs   
* problème : `assets_loader` ne permet pas de changer leurs tailles ? ajouter une méthode qui s'en occupe quand map créée ?
4. #### [x] TODO #4: 
* régler bugs `render_ground()`
5. #### [x] TODO #5: 
* mettre format normal minimap ? (actuellement convertie pour avoir meme forme que l'ecran)
> plusieurs formats ajoutés
6. #### [?] TODO #6: 
* vérifier que la position de joueur sur la minimap est la bonne, vérifier qu'il n'y a pas d'erreurs dans le calcul
>  position du 'joueur' (il n'y avait même pas de joueur, c'était juste le centre de l'écran) remplacé par indicateur de caméra
7. #### [ ] TODO #7: 
* retirer `ADDED_SAFETY_TILES` parce que cette variable n'a aucun sens ??
8. #### [ ] TODO #8: 
* à chaque fois que je fais un calcul compliqué, peut-être écrire son explication en commentaire ou dans la documentation ?
9. #### [?] TODO #9: 
* peut-être mettre la taille de chaque asset dans `ASSETS_SIZES` pour ne pas avoir à le faire dans d'autres parties du code ?
> pas encore fait, est-ce qu'il y en aura besoin ou faut-il supprimer cette variable ?
10. #### [x] TODO #10: 
* représenter le cadre de l'écran sur la minimap (plutôt que le centre de l'écran) 
* (on rajoutera plus tard la position du joueur, qui ne sera pas forcément au centre de l'écran ?)
> fixed en même temps que le **TODO #6**
11. #### [x] TODO #11: 
* pourquoi le chargement de la minimap devient + long quand `TILE_SIZE` est + élevé ?? ça devrait être l'inverse non ??
> c'était parce que les tiles étaient d'abord affichées en très grand sur une surface temporaire puis rétrécies sur la minimap,
> et j'ai découvert que `pygame.transform.scale()` lag + quand le changement de taille est + important
12. #### [x] TODO #12: 
* dans rendering, à la fin de `.compute_minimap()`, il faudrait stocker `minimap_tile_size` avec sa vraie taille 
* (et non sa taille au moment où elle a été utilisée sur `big_minimap`), et donc changer le code affecté par `minimap_tile_size`
13. #### [x] TODO #13: 
* puisque que la minimap a maintenant un contour, il faudrait la décaler légérement pour voir tous les côtés de ce contour
14. #### [ ] TODO #14: 
* il faut vraiment modifier config.py, on ne peut pas se retrouver avec 200 variables à importer à la main dans chaque fichier...
15. #### [x] TODO #15: 
* déplacer ces 'TODO' dans la documentation, même ceux réalisés, pour savoir quoi faire, pour garder une trace de ce qui a été fait et pour améliorer l'organisation
> avant, les 'TODO' étaient en commentaire à la fin du fichier *src/game.py*.
16. #### [x] TODO #16: 
* pour la minimap, mettre dans config une variable `MINIMAP_FORMAT` qui permet de décider si la minimap est du format de l'écran ou d'un carré, 
* et on pourra donc remplacer la taille de `big_minimap` par taile_x (=`self.game.w`) et taille_y (=`self.game.h` ou `self.game.w` selon format) et ensuite 
* utiliser ces variables dans la suite de `compute_minimap()`. On pourra ensuite créer la minimap différemment, par exemple en la construisant déjà petite, 
* car c'est un peu bizarre de la faire grande puis de la rétrécir. Cela permettra peut-être un gain de performance.
> tout a été fait, il y a maintenant différents formats de minimap et `compute_minimap()` a été optimisé.
> les formats sont des ratios, comme par exemple `(1, 0.75)` qui correspond à une longeur de ratio 1 et et une largeur de ratio 0.75.
> par exemple, le format `(1, 1)` donne une minimap de forme carrée
17. #### [ ] TODO #17: 
* quand `TILE_SIZE` est trop petite (donc quand les tiles ne remplissent pas tout l'écran), il y a des bugs. 
* Il faut soit fix ces bugs soit empêcher `TILE_SIZE` d'être plus petit que `self.game.w / self.blocks_size[0]` (par exemple)
18. #### [ ] TODO #18: 
* fix l'indicateur de camera, j'ai l'impression qu'il est affiché un peu trop à droite 
* (quand l'écran est centré sur un objet, l'indicateur montre que l'objet dépasse à gauche...)
* (très difficile à voir car différence de quelques pixels mais ce serait bien de savoir d'où vient le problème)
19. #### [ ] TODO #19:
* update la documentation, parce qu'au final je n'ai pas du tout suivi le plan du *README.md*. Essayer d'expliquer ce que j'ai fait,
* et peut-être en profiter pour faire et ajouter le **TODO #8**.
20. #### [x] TODO #20:
* actuellement, quand je charge les décors, je remplace les tiles de `self.ground` par les décors présents dessus (si une tile à un décor). 
* faut-il faire autrement ? Faut-il stocker la tile ET le décor ?
> maintenant, les tiles sont stockées dans `self.world_storage['ground']`, et les décors dans `self.world_storage['decors']`.
21. #### [ ] TODO #21:
* je ne sais pas encore combien d'informations une tile contiendra, mais faut-il la transformer en objet (avec une classe) ?
* ou faut-il juste stocker quelques informations sur elle ? 
22. #### [?] TODO #22:
* actuellement, les tiles sont stockées dans `self.ground`, qui est une liste de sous-listes, chaque sous-liste étant une rangée de tiles.
* faut-il remplacer ce système par un dictionnaire (avec les coordonées en clé et la tile en valeur) ?
> je ne sais toujours pas si il faudrait passer à un dictionnaire, mais cette liste est maintenant stockée dans `self.world_storage['ground']`.
23. #### [ ] TODO #23:
* essayer de rendre certains éléments arrondis sur les bords (par exemple, les chemins), comme dans la vidéo de présentation du jeu
24. #### [x] TODO #24:
* dans la classe `World`, les méthodes `load_[insert_name]()` se ressemblent beaucoup. 
* peut-être faire une seule méthode `load()` qui prend juste en argument le `file_path` et le `loading_bar_title` ?
> les méthodes `load_ground()`, `load_decors()` et `load_objects()` ont été remplacées par `load_things()`.
25. #### [x] TODO #25:
* dans `rendering`, les méthodes `.render_ground()` et `.render_objects()` sont assez similaires.
* faire une fonction commune pour éviter de répéter du code ?
> les méthodes ont été remplacées par `.render_things()`.
26. #### [ ] TODO #26:
* que ce soit pour les noms de variables, des fonctions, des classes, des fichiers ou des dossiers, ou que ce soit pour la documentation ou les commenatires,
* il faudrait choisir une seule langue, et arrêter de mélanger anglais et français.
27. #### [ ] TODO #27:
* pour l'instant tous les objets font la taille d'une tile, mais certains doivent avoir une taille différent (ex : une maison).
* utiliser `ASSETS_SIZES` ou faire autrement ?
28. #### [ ] TODO #28:
* afficher les lieux importants sur la minimap ?
29. #### [ ] TODO #29:
* il faudrait vraiment organiser tous ces **TODO** autrement que dans l'ordre auquel j'y ai pensé, 
* et les trier par type (non fait / moitié fait / fait) et par catégorie (donc selon le module, par exemple world.py, rendering.py, etc.)
30. #### [x] TODO #30:
* pour `loading_bar_console()`, peut-être afficher à la fin le temps qu'a pris le chargement ? 
* ça à l'air d'un petit défi intéressant et ça permettrai de mieux voir le lag
> file *src/ui/loading_bar_console.py* replaced by *src/task*, which handles 'tasks'. 
> a task is just a title, a timer and a progress, all of which can be seen with a loading bar.
31. #### [ ] TODO #31:
* améliorer les commits !! 
* ils doivent avoir un nom + explicite, 
* ils n'ont pas besoin d'être numérotés,
* ils peuvent être séparé en catégories (par exemple : les commits stables et les commits instables, quand on veut sauvegarder l'état actuel même si il y a des bugs)
* on peut faire d'autres branches quand on n'est pas sûr
* il faut faire + de commits !! un commit qui s'appelle "documentation update" ne doit changer que la documentation.
32. #### [ ] TODO #32:
* try to prevent the camera indicator from going outside the minimap (sometimes it's too big and it goes past the minimap border).
33. #### [?] TODO #33:
* make the player, and please don't mess up.
> player made, but there are are lots of things to improve and to add.
> currently, the player is just rendered and can move (the camera has been centered on the player), and it has basic animations and collision.
34. #### [ ] TODO #34:
* fix camera and player movement by using pythagorean theorem maybe ?
35. #### [ ] TODO #35:
* optimize the `.render_prio()` method (in `rendering.py`).
36. #### [ ] TODO #36:
* improve the player (add features + fix the current ones : optimize, simplify...) (use values from `config.py` instead of local variables, for example).
* we need to add a real hitbox, an inventory, an UI, other stats, etc.
37. #### [ ] TODO #37;
* problème : les objets montrés en priorités peuvent passer au-dessus d'autres objets quand le joueur s'approche (parce qu'ils sont redessinés). comment faire ?
38. #### [?] TODO #38:
* lots of changes to make, i think we need to turn every object into a `Collider`.
* we also need to make an `EntityHandler`. The `World` class will store the colliders (or maybe a new `ColliderHandler` class ?), the `EntityHandler` the entities.
> now, the `World` class stores both colliders and entities.
39. #### [x] TODO #39:
* for calculating an entity's movement, should we use a `pygame.math.Vector2` instead of just `dx` and `dy` ?
40. #### [?] TODO #40:
* instead of initializing some values divided by `EXPECTED_DELTA` (in `config.py`), maybe we should just pass `delta / EXPECTED_DELTA` as an argument (instead of just `delta`)
> actually, I dont think we need to pass `delta / EXPECTED_DELTA`, we only need to pass `delta / 1000`, because before it was in milliseconds but it needs to be in seconds
41. #### [?] TODO #41:
* improve the collision system
> well... I mean... it's improved, right ? :)
42. #### [ ] TODO #42:
* maybe reorganize variables in `config.py`
43. #### [ ] TODO #43:
* pour la direction de l'asset du joueur, peut-être comparer dx et dy et utiliser le + élevé en priorité (plutot que juste dy)

<br>
<br>

## Ces TODO sont à part car il servent à savoir si certains éléments du projet sont à jour ou non.
#### [ ] TODO #bonus_1:
* documentation à jour ?
> il ne faut pas oublier de le décocher quand le code est modifié.
#### [ ] TODO #bonus_2:
* delta utilisé là où il le faut ?
> pour ne pas oublier d'utiliser delta pour les valeurs qui sont modifiées à chaque frame
> do we have to use delta for the player animations ?
#### [ ] TODO #bonus_3:
* actuellement, le code est mal modularisé et documenté. 
* la structure actuelle relie les classes entre elles à travers `Game`, mais cela ne sert à rien parce qu'elles vont 'chercher' des valeurs elles-mêmes plutôt que des les 'demander'.
* par exemple, `Rendering` utilise `self.game.world.world_storage['ground']` plutôt que quelque chose comme `self.game.get_ground()`, ce qui permettrai moins de bugs et une structure + modularisée
> le code doit être bien modularisé
> le code doit être bien commenté et documenté
> le code doit être bien typé

