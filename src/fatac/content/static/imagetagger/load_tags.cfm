
<!--- Define the request variables. --->
<cfparam name="url.photoID" type="string" />


<!--- Load the tags with the given photo ID. --->
<cfset tags = application.photoTagService.getTagsByPhotoID(
	url.photoID
	) />
	

<!--- Convert the response to binary for streaming. --->
<cfset binaryResponse = toBinary( 
	toBase64(
		serializeJSON( tags )
		) 
	) />
	
<!--- Set the response headers. --->
<cfheader
	name="content-length"
	value="#arrayLen( binaryResponse )#"
	/>
	
<!--- Stream the content API response back to client. --->
<cfcontent	
	type="application/x-json"
	variable="#binaryResponse#"
	/>