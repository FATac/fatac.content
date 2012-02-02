
<!--- Define the request variables. --->
<cfparam name="url.id" type="string" />


<!--- Delete the given tag. --->
<cfset application.photoTagService.deleteTag( url.id ) />
	

<!--- Convert the response to binary for streaming. --->
<cfset binaryResponse = toBinary( 
	toBase64(
		serializeJSON( url.id )
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