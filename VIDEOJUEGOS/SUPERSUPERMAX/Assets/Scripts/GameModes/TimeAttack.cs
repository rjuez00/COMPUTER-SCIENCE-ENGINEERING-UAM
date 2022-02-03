using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Events;
using UnityEngine.SceneManagement;


[RequireComponent(typeof(AudioSource))]
public class TimeAttack : MonoBehaviour
{
    public Text timerText;
    public Text bestTimerText;

    public Text finishMsg;
    static float timer;
    private bool updateTimer = true;

    AudioSource endingMusic;


    void Start()
    {
        timer = 0;
        if (bestTimerText != null)
        {
            float besttimer = PlayerPrefs.GetFloat(SceneManager.GetActiveScene().name + "_best_score");

            int minutes = Mathf.FloorToInt(besttimer / 60);
            int seconds = Mathf.FloorToInt(besttimer - minutes * 60);
            int millis = Mathf.FloorToInt((besttimer - minutes * 60 - seconds) * 1000);

            bestTimerText.text = string.Format("{0:00}:{1:00}.{2:000}", minutes, seconds, millis);
        }
    }

    // Updates the timer on screen
    void Update()
    {
        if (updateTimer)
        {
            timer += Time.deltaTime;

            int minutes = Mathf.FloorToInt(timer / 60);
            int seconds = Mathf.FloorToInt(timer - minutes * 60);
            int millis = Mathf.FloorToInt((timer - minutes * 60 - seconds) * 1000);

            timerText.text = string.Format("{0:00}:{1:00}.{2:000}", minutes, seconds, millis);
        }
    }

    // The notUsed parameter is needed because other gamemode finishing functions (for example the race one needs the number of laps)
    public void EndTimeAttack()
    {
        updateTimer = false;

        int minutes = Mathf.FloorToInt(timer / 60);
        int seconds = Mathf.FloorToInt(timer - minutes * 60);
        int millis = Mathf.FloorToInt((timer - minutes * 60 - seconds) * 1000);

        finishMsg.text = string.Format("Finished the race in {0:00}:{1:00}.{2:000}", minutes, seconds, millis);

        // Coin reward
        int currCoins = PlayerPrefs.GetInt("coins");
        int newCoins = Mathf.Max(1350 - Mathf.RoundToInt(250 * (timer / 60)), 50);
        currCoins += newCoins;
        PlayerPrefs.SetInt("coins", currCoins);
        finishMsg.text += string.Format("\nYou won {0} coins!", newCoins);


        float bestscore = PlayerPrefs.GetFloat(SceneManager.GetActiveScene().name + "_best_score", 0f);
        if (bestscore <= 1f || bestscore > timer) PlayerPrefs.SetFloat(SceneManager.GetActiveScene().name + "_best_score", timer);



        endingMusic = GetComponent<AudioSource>();
        endingMusic.Play(0);
        // Takes the Player to the lobby after a 5 second timer
        StartCoroutine(WaitAndLeave(5));

    }

    private IEnumerator WaitAndLeave(float waitTime)
    {

        yield return new WaitForSeconds(waitTime);
        SceneLoader.LoadLevel("Lobby");
    }

}
