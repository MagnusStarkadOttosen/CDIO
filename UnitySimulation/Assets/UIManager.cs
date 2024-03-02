using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class UIManager : MonoBehaviour
{
    public TextMeshProUGUI ballCount;

    public void UpdateBallCount(int count)
    {
        ballCount.text = $"Balls Collected: {count}";
    }
}
