// Code to be refactored for ChatGPT lab
// Kamil

#include <iostream>
#include <unordered_map>
#include <string>
#include <stack>

void searchSubstrings(std::unordered_map<std::string, int> &foundSubstrings, std::unordered_map<std::string, int> wordList,
                      std::string &targetString, int startPosition, int wordLength, std::string currentSubstring);
// Displays all found substrings and their counts
void displaySubstrings(const std::unordered_map<std::string, int> &substringCounts);

int main()
{
    // Data structures to store word frequency and substring counts
    std::unordered_map<std::string, int> wordFrequencyMap;
    std::unordered_map<std::string, int> substringCountMap;

    // Input target string
    std::cout << "Enter target string: ";
    std::string targetString;
    std::cin >> targetString;

    // Input list of words
    std::cout << "Enter list of words (type 'END' to finish):\n";
    std::string inputWord;
    std::cin >> inputWord;

    // "END" signifies the end of the list (not included in list)
    while (inputWord != "END")
    {
        wordFrequencyMap[inputWord]++;
        std::cin >> inputWord;
    }

    int wordLength = wordFrequencyMap.begin()->first.size();
    std::cout << "List of substrings :\n";
    // Search for substrings
    while (targetString.size() >= wordLength)
    {
        // Iterate through the word frequency map
        for (auto mapIter = wordFrequencyMap.begin(); mapIter != wordFrequencyMap.end(); ++mapIter)
        {
            // Find the position of the word in the target string
            auto foundPosition = targetString.find(mapIter->first);
            if (foundPosition != std::string::npos)
                searchSubstrings(substringCountMap, wordFrequencyMap, targetString, foundPosition, wordLength, mapIter->first);
        }
        targetString.erase(0, wordLength);
    }
    // Display the found substrings
    if (substringCountMap.empty())
        std::cout << "no solution\n";
    else
        displaySubstrings(substringCountMap);
    return 0;
}

/**
 * @brief Iteratively searches for substrings composed of words from a word list.
 *
 * Iteratively searches for substrings within a target string that are composed of
 * words from a given word list. Counts the occurrences of each found substring.
 *
 * @param substringCounts An unordered_map (passed by reference) to store the counts of
 *        found substrings. Keys are the substrings, values are their counts.
 * @param wordList An unordered_map containing the words to search for.
 * @param targetString The string to search within.
 * @param wordLength The length of the words in the word list.
 *
 * @note This function modifies the `substringCounts` map to store substring counts.
 * @note Assumes all words in the `wordList` have the same length (`wordLength`).
 * @note Assumes the `targetString` contains sufficient characters for potential substrings.
 */
void searchSubstrings(std::unordered_map<std::string, int> &substringCounts,
                      std::unordered_map<std::string, int> &wordList,
                      std::string &targetString, int wordLength)
{
    // Stack to store the search state
    std::stack<std::pair<int, std::string>> searchStack;
    // Start with an empty substring at index 0
    searchStack.push({0, ""});
    // iterate until no more substrings can be found
    while (!searchStack.empty())
    {
        auto [index, currentSubstring] = searchStack.top();
        searchStack.pop();
        // Check if all words found (base case)
        if (wordList.empty())
        {
            substringCounts[currentSubstring]++;
            continue;
        }
        // Get the next word
        std::string nextWord = targetString.substr(index, wordLength);
        // Iterate through remaining words and push on stack
        for (auto &wordEntry : wordList)
        {
            if (wordEntry.first == nextWord)
            {
                searchStack.push({index + wordLength, currentSubstring + nextWord});
                break;
            }
        }
    }
}

/**
 * @brief Prints substrings and their counts from a map.
 *
 * Iterates over an unordered_map, `substringCounts`, printing each key-value pair where the key is a substring
 * and the value is its occurrence count. Output format is "<substring> - Count: <count>". The iteration order
 * is based on the map's internal hash table, hence unordered.
 *
 * @param substringCounts An unordered_map with std::string keys (substrings) and int values (counts). Assumes
 *        the map is non-empty; an empty map results in no output.
 *
 * @note This function produces output to std::cout and modifies no inputs.
 */
void displaySubstrings(const std::unordered_map<std::string, int> &substringCounts)
{
    for (const auto &pair : substringCounts)
        std::cout << pair.first << " - Count: " << pair.second << '\n';
}
