interface ComplexityResult {
    score: number;
    level: 'Low' | 'Medium' | 'High';
    factors: {
      length: number;
      uniqueWords: number;
      averageWordLength: number;
      specialCharacters: number;
    };
  }
  
  export function analyzeComplexity(text: string): ComplexityResult {
    const words = text.trim().split(/\s+/);
    const uniqueWords = new Set(words.map(word => word.toLowerCase()));
    const specialCharacters = (text.match(/[^a-zA-Z0-9\s]/g) || []).length;
  
    const factors = {
      length: text.length,
      uniqueWords: uniqueWords.size,
      averageWordLength: words.reduce((sum, word) => sum + word.length, 0) / words.length || 0,
      specialCharacters,
    };
  
    const lengthScore = Math.min(factors.length / 500, 1) * 25;
    const uniqueWordsScore = Math.min(factors.uniqueWords / 100, 1) * 25;
    const avgWordLengthScore = Math.min(factors.averageWordLength / 10, 1) * 25;
    const specialCharactersScore = Math.min(specialCharacters / 50, 1) * 25;
  
    const totalScore = lengthScore + uniqueWordsScore + avgWordLengthScore + specialCharactersScore;
  
    let level: 'Low' | 'Medium' | 'High';
    if (totalScore < 33) {
      level = 'Low';
    } else if (totalScore < 66) {
      level = 'Medium';
    } else {
      level = 'High';
    }
  
    return {
      score: totalScore,
      level,
      factors,
    };
  }