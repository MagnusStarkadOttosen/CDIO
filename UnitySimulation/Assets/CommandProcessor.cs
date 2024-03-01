using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CommandProcessor : MonoBehaviour
{

    public GameObject robot;

    public void ProcessCommand(string command)
    {
        string[] commandParts = command.Split(' ');

        string action = commandParts[0].ToLower();

        if (float.TryParse(commandParts[1], out float value))
        {
            switch (action)
            {
                case "move":
                    Move(value);
                    break;
                //add more robot commands here
                default:
                    Debug.LogWarning($"Unknown Command {action}");
                    break;
            }
        }
        else
        {
            Debug.LogWarning($"Invalid command parameter: {commandParts[1]}");
        }
    }

    public void Move(float distance)
    {
        Vector3 direction = robot.transform.forward * distance;
        robot.transform.position += direction;
        Debug.Log($"Moved robot forward by {distance} units.");
    }
}
