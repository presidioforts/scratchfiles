Sub ExtractEmailsFromTrainingFolder()
    Dim olApp As Outlook.Application
    Dim olNamespace As Outlook.Namespace
    Dim olInbox As Outlook.MAPIFolder
    Dim olFolder As Outlook.MAPIFolder
    Dim olItem As Object
    Dim fileNum As Integer

    ' Set Outlook objects
    Set olApp = Outlook.Application
    Set olNamespace = olApp.GetNamespace("MAPI")
    
    ' Set olInbox to the Inbox folder and then get the "Training" subfolder
    Set olInbox = olNamespace.GetDefaultFolder(olFolderInbox)
    Set olFolder = olInbox.Folders("Training")

    ' Open text file for output
    fileNum = FreeFile
    Open "C:\Temp\EmailAddresses.txt" For Output As #fileNum

    ' Loop through items in the "Training" folder
    For Each olItem In olFolder.Items
        If TypeOf olItem Is MailItem Then
            Print #fileNum, olItem.SenderEmailAddress
        End If
    Next olItem

    ' Close the file and confirm export
    Close #fileNum
    MsgBox "Email addresses have been exported."
End Sub
