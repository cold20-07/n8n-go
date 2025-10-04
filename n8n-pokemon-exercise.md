# n8n Pokémon API Exercise

This exercise demonstrates data transformation in n8n using the PokéAPI.

## Step 1: HTTP Request Node Configuration

**Node Settings:**
- Method: GET
- URL: `https://pokeapi.co/api/v2/pokemon`
- Authentication: None required

**Expected Response Structure:**
```json
{
  "count": 1302,
  "next": "https://pokeapi.co/api/v2/pokemon/?offset=20&limit=20",
  "previous": null,
  "results": [
    {
      "name": "bulbasaur",
      "url": "https://pokeapi.co/api/v2/pokemon/1/"
    },
    {
      "name": "ivysaur", 
      "url": "https://pokeapi.co/api/v2/pokemon/2/"
    }
    // ... more pokemon
  ]
}
```

## Step 2: Transform with Split Out Node

**Split Out Node Configuration:**
- Field to Split Out: `results`
- Include: `Keep Only Set Key`

This will convert the single item containing an array of 20 Pokémon into 20 separate items, each containing one Pokémon.

**Result after Split Out:**
Each item will look like:
```json
{
  "name": "bulbasaur",
  "url": "https://pokeapi.co/api/v2/pokemon/1/"
}
```

## Step 3: Transform with Code Node (Alternative Method)

**Code Node Configuration:**
- Execution Mode: `Run Once for All Items`

**JavaScript Code:**
```javascript
// Get the first item from HTTP Request (contains the full API response)
const apiResponse = $input.first().json;

// Extract the results array and transform each pokemon into n8n format
return apiResponse.results.map(pokemon => {
  return {
    json: {
      name: pokemon.name,
      url: pokemon.url,
      // Extract pokemon ID from URL for convenience
      id: pokemon.url.split('/').slice(-2, -1)[0]
    }
  };
});
```

**Enhanced Code Node (with additional data extraction):**
```javascript
// Get the API response
const apiResponse = $input.first().json;

// Transform and enhance the data
return apiResponse.results.map((pokemon, index) => {
  // Extract ID from URL
  const pokemonId = pokemon.url.split('/').slice(-2, -1)[0];
  
  return {
    json: {
      id: parseInt(pokemonId),
      name: pokemon.name,
      url: pokemon.url,
      // Add some computed fields
      capitalizedName: pokemon.name.charAt(0).toUpperCase() + pokemon.name.slice(1),
      position: index + 1
    }
  };
});
```

## Comparison: Split Out vs Code Node

### Split Out Node:
- **Pros**: No coding required, simple configuration
- **Cons**: Limited data transformation capabilities
- **Use case**: When you just need to split arrays without modification

### Code Node:
- **Pros**: Full control over data transformation, can add computed fields
- **Cons**: Requires JavaScript knowledge
- **Use case**: When you need to modify, enhance, or restructure data during splitting

## Expected Final Output

After either transformation method, you should have 20 items (one per Pokémon) instead of 1 item with an array of 20 Pokémon.

Each item structure:
```json
{
  "id": 1,
  "name": "bulbasaur",
  "url": "https://pokeapi.co/api/v2/pokemon/1/",
  "capitalizedName": "Bulbasaur",
  "position": 1
}
```