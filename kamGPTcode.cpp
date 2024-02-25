// Code to be refactored for ChatGPT lab
// Kamil

#include <iostream>
#include <unordered_map>
#include <string>

void searchSubstrings(std::unordered_map<std::string, int>& foundSubstrings, std::unordered_map<std::string, int> wordList, 
                      std::string &targetString, int startPosition, int wordLength, std::string currentSubstring);
void displaySubstrings(std::unordered_map<std::string, int>::iterator iter, std::unordered_map<std::string, int>& substringCounts);

int main()
{
    std::unordered_map<std::string, int> wordFrequencyMap;
    std::unordered_map<std::string, int> substringCountMap;

    // Input target string
    std::cout << "Enter mega word:";
    std::string targetWord;
    std::cin >> targetWord;

    // Input list of words
    std::cout << "Enter list of words:\n";
    std::string inputWord;
    std::cin >> inputWord;

    // "END" signifies the end of the list (not included in list)
    while (inputWord != "END")
    {
        wordFrequencyMap[inputWord]++;
        std::cin >> inputWord;
    }

    int firstWordLength = wordFrequencyMap.begin()->first.size();

    std::cout << "List of substrings :\n";

    while(targetWord.size() >= firstWordLength)
    {
        for (auto mapIter = wordFrequencyMap.begin(); mapIter != wordFrequencyMap.end(); ++mapIter)
        {
            auto foundPosition = targetWord.find(mapIter->first);

            if (foundPosition != std::string::npos)
            {
                searchSubstrings(substringCountMap, wordFrequencyMap, targetWord, foundPosition, firstWordLength, mapIter->first);
            }
        }
        targetWord.erase(0, firstWordLength);
    }
    if (substringCountMap.empty())
        std::cout << "no solution\n";
    else
        displaySubstrings(substringCountMap.begin(), substringCountMap);
    return 0;
}

void searchSubstrings(std::unordered_map<std::string, int>& substringCounts, std::unordered_map<std::string, int> wordList,
                      std::string &targetString, int index, int wordLength, std::string currentSubstring)
{
    std::string foundWord = targetString.substr(index, wordLength);
    wordList.erase(foundWord);
    
    index += wordLength;

    if (wordList.empty())
    {
        substringCounts[currentSubstring]++;
        return;
    }

    std::string nextWord = targetString.substr(index, wordLength);
    for (auto listIter = wordList.begin(); listIter != wordList.end(); ++listIter)
    {
        if(nextWord == listIter->first)
            searchSubstrings(substringCounts, wordList, targetString, index, wordLength, currentSubstring+nextWord);
    }
}

void displaySubstrings(std::unordered_map<std::string, int>::iterator iter, std::unordered_map<std::string, int>& substringCounts)
{
    if (iter == substringCounts.end())
        return;
    std::unordered_map<std::string, int>::iterator nextIter = iter;
    nextIter++;
    displaySubstrings(nextIter, substringCounts);
    std::cout << iter->first << "\n";
    return;
}
