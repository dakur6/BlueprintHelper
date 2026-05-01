import blueprint

structure1 = blueprint.load(r"c:\Users\cl4m1\OneDrive\Документы\My Games\Sprocket\Factions\БТР\Blueprints\Plate Structures\cache.blueprint")
structure2 = blueprint.load(r"c:\Users\cl4m1\OneDrive\Документы\My Games\Sprocket\Factions\БТР\Blueprints\Plate Structures\cache 1.blueprint")
structure1.join(structure2)

blueprint.save(structure1, r"c:\Users\cl4m1\OneDrive\Документы\My Games\Sprocket\Factions\БТР\Blueprints\Plate Structures\cache.blueprint")