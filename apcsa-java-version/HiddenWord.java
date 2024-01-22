public class HiddenWord {
    private String word;
    public HiddenWord(String word) {
        this.word = word;
    }
    public String getHint(String guess) {
        String hint = "";
        for (int i = 0; i < guess.length(); i++) {
            if (guess.substring(i, i + 1).equals(word.substring(i, i+1))) {
                hint += guess.substring(i, i+1);
                continue;
            }
            if (word.indexOf(guess.substring(i, i+1)) >= i) {
                hint += "+";
                continue;
            }
            hint += "*";
        }
        return hint;
    }
}