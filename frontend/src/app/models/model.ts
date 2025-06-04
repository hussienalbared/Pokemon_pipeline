
interface PokemonAbility {
  name: string;
  is_hidden: boolean;
}

interface PokemonStat {
  name: string;
  base_stat: number;
  effort: number;
}

interface Pokemon {
  id: number;
  name: string;
  base_experience: number;
  height: number;
  weight: number;
  types: string[];
  abilities: PokemonAbility[];
  stats: PokemonStat[];
}
