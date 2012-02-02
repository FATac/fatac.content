
<!--- Define the request variables. --->
<cfparam name="url.id" type="string" default="" />
<cfparam name="url.x" type="numeric" />
<cfparam name="url.y" type="numeric" />
<cfparam name="url.width" type="numeric" />
<cfparam name="url.height" type="numeric" />
<cfparam name="url.message" type="string" />
<cfparam name="url.photoID" type="string" />


<!--- Save the given tag and get the new / exisitng tag ID. --->
<cfset tagID = application.photoTagService.saveTag(
	url.id,
	url.x,
	url.y,
	url.width,
	url.height,
	url.message,
	url.photoID
	) />
	

<!--- Convert the response to binary for streaming. --->
<cfset binaryResponse = toBinary( 
	toBase64(
		serializeJSON( tagID )
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