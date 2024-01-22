// Gabi Natenshon 11/2/23
import java.util.Scanner;
public class Main {
  public static void main(String[] args) {
    HiddenWord puzzle = new HiddenWord("HARPS");
    Scanner input = new Scanner(System.in);
    String guess, hint;
    System.out.println("Enter a 5 letter word, press X to stop");
    while (true) {
      guess = input.nextLine().toUpperCase();
      hint = puzzle.getHint(guess);
      if (guess.equals("X") || hint.equals(guess)) {
        System.out.println("Thanks for playing!");
        break;
      }
      System.out.println(hint);
      System.out.println("Try again, enter a 5 letter word, press X to stop");
    }
    System.out.println("Made by Gabi Natenshon");
  }
}