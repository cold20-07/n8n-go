// n8n Code Node Examples for Pokémon API Exercise

// ===== BASIC TRANSFORMATION =====
// Simple transformation to split results array into individual items
function basicTransformation() {
  const apiResponse = $input.first().json;
  
  return apiResponse.results.map(pokemon => {
    return {
      json: {
        name: pokemon.name,
        url: pokemon.url
      }
    };
  });
}

// ===== ENHANCED TRANSFORMATION =====
// Enhanced version with additional computed fields
function enhancedTransformation() {
  const apiResponse = $input.first().json;
  
  return apiResponse.results.map((pokemon, index) => {
    // Extract ID from URL (e.g., "https://pokeapi.co/api/v2/pokemon/1/" -> "1")
    const pokemonId = pokemon.url.split('/').slice(-2, -1)[0];
    
    return {
      json: {
        id: parseInt(pokemonId),
        name: pokemon.name,
        url: pokemon.url,
        capitalizedName: pokemon.name.charAt(0).toUpperCase() + pokemon.name.slice(1),
        position: index + 1,
        // Add API endpoint for detailed info
        detailsEndpoint: `https://pokeapi.co/api/v2/pokemon/${pokemonId}/`
      }
    };
  });
}

// ===== FILTERED TRANSFORMATION =====
// Filter and transform (e.g., only Pokémon with names starting with 'b')
function filteredTransformation() {
  const apiResponse = $input.first().json;
  
  return apiResponse.results
    .filter(pokemon => pokemon.name.startsWith('b'))
    .map(pokemon => {
      const pokemonId = pokemon.url.split('/').slice(-2, -1)[0];
      
      return {
        json: {
          id: parseInt(pokemonId),
          name: pokemon.name,
          url: pokemon.url,
          startsWithB: true
        }
      };
    });
}

// ===== GROUPED TRANSFORMATION =====
// Group Pokémon by first letter of name
function groupedTransformation() {
  const apiResponse = $input.first().json;
  const grouped = {};
  
  // Group by first letter
  apiResponse.results.forEach(pokemon => {
    const firstLetter = pokemon.name.charAt(0).toLowerCase();
    if (!grouped[firstLetter]) {
      grouped[firstLetter] = [];
    }
    grouped[firstLetter].push(pokemon);
  });
  
  // Convert to n8n format
  return Object.keys(grouped).map(letter => {
    return {
      json: {
        letter: letter.toUpperCase(),
        count: grouped[letter].length,
        pokemon: grouped[letter].map(p => ({
          name: p.name,
          id: p.url.split('/').slice(-2, -1)[0]
        }))
      }
    };
  });
}

// ===== ACTUAL CODE FOR N8N CODE NODE =====
// Copy this into your n8n Code node:

const apiResponse = $input.first().json;

return apiResponse.results.map((pokemon, index) => {
  const pokemonId = pokemon.url.split('/').slice(-2, -1)[0];
  
  return {
    json: {
      id: parseInt(pokemonId),
      name: pokemon.name,
      url: pokemon.url,
      capitalizedName: pokemon.name.charAt(0).toUpperCase() + pokemon.name.slice(1),
      position: index + 1
    }
  };
});