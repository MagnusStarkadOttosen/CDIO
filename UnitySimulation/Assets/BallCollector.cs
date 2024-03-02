using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BallCollector : MonoBehaviour
{
    private int ballCount = 0;
    public UIManager uiManager;

    private void OnTriggerEnter(Collider collider)
    {
        if (collider.gameObject.CompareTag("Ball"))
        {
            ballCount++;
            Destroy(collider.gameObject);
            uiManager.UpdateBallCount(ballCount);
        }
    }
}
