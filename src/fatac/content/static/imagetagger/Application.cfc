
<cfcomponent
	output="false"
	hint="I define application settings and event handlers.">
	
	<!--- Define the application. --->
	<cfset this.name = hash( getCurrentTemplatePath() ) />
	<cfset this.applicationTimeout = createTimeSpan( 0, 0, 5, 0 ) />
	
	<!--- Define request settings. --->
	<cfsetting
		showdebugoutput="false"
		requesttimeout="5"
		/>
	
	
	<cffunction 
		name="onApplicationStart" 
		access="public" 
		returntype="boolean" 
		output="false" 
		hint="I initialize the application.">
		
		<!--- 
			Create and cache an instance of the photo tagging 
			service in the application. This will provide our 
			public API with a means to gather and persist the
			user's photo tag data.
		--->
		<cfset application.photoTagService = createObject(
			"component", "PhotoTagService"
			).init() 
			/>
	
		<!--- Return true to allow the application to load. --->
		<cfreturn true />
	</cffunction>
	
	
	<cffunction 
		name="onRequestStart" 
		access="public" 
		returntype="boolean" 
		output="false" 
		hint="I initialize the request.">
	
		<!--- Check for the application reset flag. --->
		<cfif structKeyExists( url, "reset" )>
			
			<!--- Explicitly reset the application. --->
			<cfset this.onApplicationStart() />
		
		</cfif>
		
		<!--- Return true so the page can load. --->
		<cfreturn true />
	</cffunction>
	
</cfcomponent>