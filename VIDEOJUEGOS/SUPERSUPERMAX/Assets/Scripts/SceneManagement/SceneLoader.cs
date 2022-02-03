using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneLoader : MonoBehaviour
{
    private static Action onLoaderCallback;

    public static void LoadLevel(string sceneName)
    {
        onLoaderCallback = () =>
        {
            Application.backgroundLoadingPriority = ThreadPriority.Low;
            SceneManager.LoadSceneAsync(sceneName);
        };
        SceneManager.LoadScene("Loading");
    }

    public static void LoaderCallback()
    {
        if (onLoaderCallback != null)
        {
            onLoaderCallback();
            onLoaderCallback = null;
        }
    }

}
