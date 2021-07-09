using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class MAINMENU : MonoBehaviour
{
    //The current score and the max score to display3
    public Text scoreText;
    public Text max_score_text;

    private static int cur_score, max_score;

    private void Start()
    {
        if(scoreText != null && max_score_text!=null)
        {
        scoreText.text = "Current Score: " + cur_score;
        max_score_text.text = "Max Score: " + max_score;
        }

    }
    public static void UpdateScoreText(int cur, int max)
    {
        cur_score = cur;
        max_score = max;
    }
    public void playGame()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);

    }


    public void quitGame()
    {
        Debug.Log("QUIT");
        Application.Quit();
    }

    public void playAgain()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex - 1);
    }

}