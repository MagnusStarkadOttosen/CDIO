using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CommandProcessor : MonoBehaviour
{

    public GameObject robot;
    private Vector3 targetPosition;
    private Quaternion targetRotation;
    private bool isMoving = false;
    private bool isRotating = false;
    public float moveSpeed = 5.0f;
    public float rotateSpeed = 90.0f;

    void Start()
    {
        targetPosition = robot.transform.position;
    }

    void Update()
    {
        if (isMoving)
        {
            robot.transform.position = Vector3.MoveTowards(robot.transform.position, targetPosition, moveSpeed * Time.deltaTime);
            if(robot.transform.position == targetPosition)
            {
                isMoving = false;
            }
        }
        if (isRotating)
        {
            robot.transform.rotation = Quaternion.RotateTowards(robot.transform.rotation, targetRotation, rotateSpeed * Time.deltaTime);
            if (robot.transform.rotation == targetRotation)
            {
                isRotating = false;
            }
        }
    }

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
                case "rotate":
                    Rotate(value);
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
        targetPosition = robot.transform.position + robot.transform.forward * distance;
        isMoving = true;
        Debug.Log($"Moved robot forward by {distance} units.");
    }

    public void Rotate(float degrees)
    {
        targetRotation = Quaternion.Euler(robot.transform.eulerAngles + new Vector3(0, degrees, 0));
        isRotating = true;
    }
}
